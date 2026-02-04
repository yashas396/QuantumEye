"""
QuantumEye v2.0 - Flask Backend
Connects the real qdt_fraud_model (VQAE) to the frontend dashboard.

Architecture:
  Input(4 PCA) → fc_in(4→4) → QuantumCircuit(4q,10L) → Measure(16 probs) → fc_out(16→4) → MSE
"""

import os, json, math, time, threading, pickle
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

# Qiskit integration (optional — graceful degradation if not installed)
try:
    from qiskit_backend import (
        build_vqae_circuit,
        run_aer_statevector,
        run_aer_sampler,
        IBMQuantumManager,
    )
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False

# ─── Configuration ───────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "qdt_fraud_model")
CSV_PATH = os.path.join(BASE_DIR, "creditcard.csv")
N_QUBITS = 4
N_LAYERS = 10
N_STATES = 2 ** N_QUBITS          # 16
BASE_THRESHOLD = 0.0083
PCA_COMPONENTS = 4
NORMAL_SAMPLE = 5000               # calibration sample size

app = Flask(__name__, static_folder=BASE_DIR)
CORS(app)


# ─── Quantum Gate Matrices (numpy, complex128) ──────────────────────
I2 = np.eye(2, dtype=np.complex128)

def ry_matrix(theta):
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=np.complex128)

def rx_matrix(theta):
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    return np.array([[c, -1j * s], [-1j * s, c]], dtype=np.complex128)

def rz_matrix(theta):
    return np.array([[np.exp(-1j * theta / 2), 0],
                     [0, np.exp(1j * theta / 2)]], dtype=np.complex128)

def _kron_list(mats):
    """Kronecker product of a list of matrices."""
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out

def _single_qubit_gate(gate_2x2, qubit, n_qubits):
    """Expand a single-qubit gate to full N-qubit unitary."""
    mats = [I2] * n_qubits
    mats[qubit] = gate_2x2
    return _kron_list(mats)

def _cnot_gate(ctrl, tgt, n_qubits):
    """Build CNOT unitary for N qubits."""
    dim = 2 ** n_qubits
    U = np.zeros((dim, dim), dtype=np.complex128)
    for i in range(dim):
        bits = list(format(i, f'0{n_qubits}b'))
        if bits[ctrl] == '0':
            U[i, i] = 1.0
        else:
            bits[tgt] = '1' if bits[tgt] == '0' else '0'
            j = int(''.join(bits), 2)
            U[j, i] = 1.0
    return U

# Pre-compute CNOT gates (they're fixed)
CNOT_GATES = []
for q in range(N_QUBITS):
    ctrl_q = q
    tgt_q = (q + 1) % N_QUBITS
    CNOT_GATES.append(_cnot_gate(ctrl_q, tgt_q, N_QUBITS))


# ─── Load Model Weights ─────────────────────────────────────────────
def load_model_weights():
    """Load the state dict from the loose-file torch save format."""
    pkl_path = os.path.join(MODEL_DIR, "data.pkl")
    data_dir = MODEL_DIR

    class _Loader(pickle.Unpickler):
        def persistent_load(self, saved_id):
            _tag, _cls, key, _loc, numel = saved_id
            fpath = os.path.join(data_dir, "data", str(key))
            nbytes = int(numel) * 4  # float32 = 4 bytes
            storage = torch.UntypedStorage.from_file(fpath, shared=False, nbytes=nbytes)
            return torch.storage.TypedStorage(wrap_storage=storage, dtype=torch.float32)

    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with open(pkl_path, "rb") as f:
            sd = _Loader(f).load()

    weights = {}
    for k, v in sd.items():
        if isinstance(v, torch.Tensor):
            weights[k] = v
    return weights


class QDTFraudModel:
    """
    Faithful reproduction of the trained QDT_Fraud model.
    Forward: x(4) → fc_in(4→4) → quantum_circuit(4q,10L) → probs(16) → fc_out(16→4) → x_hat(4)
    """

    def __init__(self, weights):
        self.params = weights["params"].numpy()          # (10, 4, 3)
        self.fc_in_w = weights["fc_in.weight"].numpy()   # (4, 4)
        self.fc_in_b = weights["fc_in.bias"].numpy()     # (4,)
        self.fc_out_w = weights["fc_out.weight"].numpy()  # (4, 16)
        self.fc_out_b = weights["fc_out.bias"].numpy()    # (4,)
        print(f"  [Model] params: {self.params.shape}")
        print(f"  [Model] fc_in:  {self.fc_in_w.shape} + bias {self.fc_in_b.shape}")
        print(f"  [Model] fc_out: {self.fc_out_w.shape} + bias {self.fc_out_b.shape}")

    def fc_in(self, x):
        return x @ self.fc_in_w.T + self.fc_in_b

    def fc_out(self, probs):
        return probs @ self.fc_out_w.T + self.fc_out_b

    def quantum_circuit(self, features):
        """
        Statevector simulation of the variational quantum circuit.
        features: numpy array of shape (4,) — output of fc_in
        Returns: probabilities array of shape (16,)
        """
        dim = N_STATES
        # Initialize |0000⟩
        state = np.zeros(dim, dtype=np.complex128)
        state[0] = 1.0

        # Angle embedding: RY(feature_i) on qubit i
        for q in range(N_QUBITS):
            gate = _single_qubit_gate(ry_matrix(features[q].item()), q, N_QUBITS)
            state = gate @ state

        # Variational layers
        for layer in range(N_LAYERS):
            # Rotations: RX, RY, RZ per qubit
            for q in range(N_QUBITS):
                rx_angle = self.params[layer, q, 0]
                ry_angle = self.params[layer, q, 1]
                rz_angle = self.params[layer, q, 2]

                gate_rx = _single_qubit_gate(rx_matrix(rx_angle), q, N_QUBITS)
                state = gate_rx @ state

                gate_ry = _single_qubit_gate(ry_matrix(ry_angle), q, N_QUBITS)
                state = gate_ry @ state

                gate_rz = _single_qubit_gate(rz_matrix(rz_angle), q, N_QUBITS)
                state = gate_rz @ state

            # CNOT ring entanglement: (0,1), (1,2), (2,3), (3,0)
            for cnot_gate in CNOT_GATES:
                state = cnot_gate @ state

        # Probabilities
        probs = np.abs(state) ** 2
        probs = probs / probs.sum()  # normalize for numerical stability
        return probs.astype(np.float32)

    def quantum_circuit_dispatch(self, features, mode='numpy'):
        """Route quantum circuit to the appropriate backend."""
        if mode == 'aer_statevector' and QISKIT_AVAILABLE:
            return run_aer_statevector(features, self.params)
        elif mode == 'aer_sampler' and QISKIT_AVAILABLE:
            return run_aer_sampler(features, self.params)
        else:
            return self.quantum_circuit(features)

    def forward(self, x, mode='numpy'):
        """
        Full forward pass.
        x: numpy array of shape (4,) — PCA features
        mode: 'numpy' | 'aer_statevector' | 'aer_sampler'
        Returns dict with all analysis results.
        """
        x_in = x.astype(np.float32)

        # fc_in
        encoded = self.fc_in(x_in)

        # Quantum circuit (dispatched by mode)
        probs = self.quantum_circuit_dispatch(encoded, mode)

        # fc_out → reconstructed
        x_hat = self.fc_out(probs)

        # Reconstruction error (MSE)
        mse = float(np.mean((x_in - x_hat) ** 2))

        # Quantum state (most probable basis state)
        max_idx = int(np.argmax(probs))
        q_state = "|" + format(max_idx, f"0{N_QUBITS}b") + "⟩"

        # Bloch sphere vector from qubit-0 marginals
        p0, p1 = 0.0, 0.0
        for i in range(N_STATES):
            if ((i >> (N_QUBITS - 1)) & 1) == 0:
                p0 += probs[i]
            else:
                p1 += probs[i]
        z = float(p0 - p1)
        theta = math.acos(max(-1, min(1, z)))
        phi = float(probs[1]) * math.pi * 4 - math.pi
        bloch = {
            "x": round(math.sin(theta) * math.cos(phi), 6),
            "y": round(math.sin(theta) * math.sin(phi), 6),
            "z": round(z, 6)
        }

        return {
            "reconError": round(mse, 8),
            "probs": probs.tolist(),
            "qState": q_state,
            "blochVec": bloch,
            "pcaFeatures": x_in.tolist(),
            "reconstructed": x_hat.tolist(),
            "encoded": encoded.tolist(),
        }


# ─── Data Pipeline (matches exact training preprocessing) ────────────
class DataPipeline:
    """
    Reproduces the EXACT preprocessing from training notebook:
    1. Subsample: 1000 normal + all 492 fraud (random_state=42)
    2. Features: ALL columns except Class (includes Time)
    3. MinMaxScaler(feature_range=(-1, 1)) fitted on subsample
    4. PCA(n_components=4) fitted on subsample
    5. Train/test split: 80/20 of normal, test = val_normal + all fraud
    """

    def __init__(self, csv_path):
        print("[Pipeline] Loading CSV...")
        self.df = pd.read_csv(csv_path)
        print(f"  Loaded {len(self.df)} rows, {len(self.df.columns)} columns")

        # ── EXACT training preprocessing ──
        # Subsample: 1000 normal + all fraud
        normal_df = self.df[self.df["Class"] == 0]
        fraud_df = self.df[self.df["Class"] == 1]
        normal_sample = normal_df.sample(n=1000, random_state=42)
        df_small = pd.concat([normal_sample, fraud_df]).reset_index(drop=True)

        # Features: ALL columns except Class (includes Time!)
        self.feature_cols = list(df_small.columns[:-1])  # everything except 'Class'
        print(f"  Features ({len(self.feature_cols)}): {self.feature_cols[:3]}...{self.feature_cols[-2:]}")

        # MinMaxScaler (-1, 1) — fitted on combined subsample
        self.scaler = MinMaxScaler(feature_range=(-1, 1))
        df_small[self.feature_cols] = self.scaler.fit_transform(df_small[self.feature_cols])

        # PCA to 4 components — fitted on combined subsample
        self.pca = PCA(n_components=PCA_COMPONENTS)
        df_pca = pd.DataFrame(
            self.pca.fit_transform(df_small[self.feature_cols]),
            columns=[f"PC{i+1}" for i in range(PCA_COMPONENTS)]
        )
        df_pca["Class"] = df_small["Class"].values
        print(f"  PCA variance ratio: {self.pca.explained_variance_ratio_.round(4).tolist()}")

        # Train/test split (same as training)
        train_normal, val_normal = train_test_split(
            df_pca[df_pca["Class"] == 0], test_size=0.2, random_state=42
        )
        self.X_train = train_normal.drop("Class", axis=1).values.astype(np.float32)
        test_mixed = pd.concat([val_normal, df_pca[df_pca["Class"] == 1]])
        self.X_test = test_mixed.drop("Class", axis=1).values.astype(np.float32)
        self.y_test = test_mixed["Class"].values

        print(f"  Train (normal): {self.X_train.shape}")
        print(f"  Test (mixed):   {self.X_test.shape} ({sum(self.y_test==0)} normal, {sum(self.y_test==1)} fraud)")

        # Build stream queue for dashboard (shuffled mix from full dataset)
        stream_normal = normal_df.sample(n=min(2000, len(normal_df)), random_state=123)
        stream_combined = pd.concat([stream_normal, fraud_df]).sample(frac=1, random_state=42)
        self.stream_queue = stream_combined.to_dict("records")
        self.stream_index = 0

        # Recent errors for dynamic threshold
        self.recent_errors = []
        self.calibrated_threshold = BASE_THRESHOLD

        print(f"  Stream queue: {len(self.stream_queue)} transactions")

        # Free the full DataFrame to save memory (keep only the row count)
        self.total_rows = len(self.df)
        del self.df

    def transform(self, row):
        """Transform a single transaction row to PCA features."""
        features = np.array([float(row.get(c, 0)) for c in self.feature_cols]).reshape(1, -1)
        scaled = self.scaler.transform(features)
        pca_out = self.pca.transform(scaled)
        return pca_out[0].astype(np.float32)

    def get_next_batch(self, batch_size=1):
        """Get next batch of transactions from stream queue."""
        results = []
        for _ in range(batch_size):
            if self.stream_index >= len(self.stream_queue):
                self.stream_index = 0
            row = self.stream_queue[self.stream_index]
            self.stream_index += 1
            results.append(row)
        return results

    def calibrate(self, model_obj):
        """
        Calibrate threshold using exact same method as training notebook:
        - Compute train errors on X_train
        - Search thresholds in linspace(train_min, train_max, 200)
        - Optimize: score = accuracy + 0.5 * f1
        """
        from sklearn.metrics import accuracy_score, f1_score

        print("[Pipeline] Computing train errors for threshold calibration...")
        train_errors = []
        for i in range(len(self.X_train)):
            result = model_obj.forward(self.X_train[i])
            train_errors.append(result["reconError"])
        train_errors = np.array(train_errors)

        print("[Pipeline] Computing test errors...")
        test_errors = []
        for i in range(len(self.X_test)):
            result = model_obj.forward(self.X_test[i])
            test_errors.append(result["reconError"])
        test_errors = np.array(test_errors)

        # Threshold search (EXACT same as notebook)
        thresholds = np.linspace(train_errors.min(), train_errors.max(), 200)
        best_score, best_threshold = 0, train_errors.mean() + 3 * train_errors.std()
        for t in thresholds:
            y_pred = (test_errors > t).astype(int)
            acc = accuracy_score(self.y_test, y_pred)
            f1 = f1_score(self.y_test, y_pred)
            score = acc + 0.5 * f1  # same weighted score as notebook
            if score > best_score:
                best_score, best_threshold = score, t

        self.calibrated_threshold = best_threshold
        self.recent_errors = list(train_errors)

        # Report metrics
        y_pred = (test_errors > best_threshold).astype(int)
        acc = accuracy_score(self.y_test, y_pred)
        f1 = f1_score(self.y_test, y_pred)

        normal_errs = test_errors[self.y_test == 0]
        fraud_errs = test_errors[self.y_test == 1]

        print(f"  Train errors  - mean: {train_errors.mean():.6f}, std: {train_errors.std():.6f}")
        print(f"  Normal errors - mean: {normal_errs.mean():.6f}")
        print(f"  Fraud errors  - mean: {fraud_errs.mean():.6f}")
        print(f"  Calibrated threshold: {best_threshold:.6f}")
        print(f"  Accuracy: {acc*100:.2f}%, F1: {f1*100:.2f}%")
        return best_threshold

    def get_dynamic_threshold(self):
        """Adaptive threshold from recent errors, centered on calibrated threshold."""
        base = self.calibrated_threshold
        if len(self.recent_errors) < 20:
            return base
        norm_errors = [e for e in self.recent_errors if e < base * 4]
        if len(norm_errors) < 10:
            return base
        mean_e = np.mean(norm_errors)
        std_e = np.std(norm_errors)
        dyn = mean_e + 3 * std_e
        return max(base * 0.5, min(base * 2, dyn))


# ─── Global State ────────────────────────────────────────────────────
model = None
pipeline = None
stats = {"total_analyzed": 0, "total_fraud": 0, "start_time": 0}

# IBM Quantum integration
ibm_manager = IBMQuantumManager() if QISKIT_AVAILABLE else None
quantum_backend_mode = 'numpy'  # 'numpy' | 'aer_statevector' | 'aer_sampler'


def _background_calibrate():
    """Run calibration in background thread so the app starts quickly."""
    global model, pipeline
    print("\n[background] Calibrating threshold (exact training method)...")
    calibrated_thresh = pipeline.calibrate(model)

    print("[background] Running validation with calibrated threshold...")
    test_rows = pipeline.get_next_batch(10)
    correct = 0
    for i, row in enumerate(test_rows):
        pca_features = pipeline.transform(row)
        result = model.forward(pca_features)
        actual = int(row.get("Class", 0))
        label = "FRAUD" if actual == 1 else "normal"
        is_fraud = result["reconError"] > calibrated_thresh
        verdict = "FRAUD" if is_fraud else "normal"
        if (actual == 1) == is_fraud:
            correct += 1
        print(f"  tx[{i}] actual={label:6s}  error={result['reconError']:.6f}  thresh={calibrated_thresh:.6f}  verdict={verdict}")
    pipeline.stream_index = 0  # reset

    print(f"\n  Validation accuracy: {correct}/{len(test_rows)} ({correct/len(test_rows)*100:.0f}%)")
    print(f"  Calibrated threshold: {round(calibrated_thresh, 6)}")
    print("[background] Calibration complete.\n")


def initialize():
    global model, pipeline, stats
    print("=" * 60)
    print("  Quantum Eye - Backend Initialization")
    print("=" * 60)

    print("\n[1/3] Loading model weights...")
    weights = load_model_weights()
    model = QDTFraudModel(weights)

    print("\n[2/3] Initializing data pipeline...")
    pipeline = DataPipeline(CSV_PATH)

    stats["start_time"] = time.time()

    print("\n[3/3] Starting background calibration...")
    threading.Thread(target=_background_calibrate, daemon=True).start()

    print("\n" + "=" * 60)
    print("  Backend ready. Serving on http://localhost:5000")
    print("  Using base threshold until calibration completes: " + str(BASE_THRESHOLD))
    print("=" * 60 + "\n")


# ─── API Routes ──────────────────────────────────────────────────────

@app.route("/")
def serve_index():
    return send_from_directory(BASE_DIR, "interface.html")


@app.route("/api/status")
def api_status():
    return jsonify({
        "status": "online",
        "model": "qdt_fraud_model",
        "qubits": N_QUBITS,
        "layers": N_LAYERS,
        "base_threshold": BASE_THRESHOLD,
        "calibrated_threshold": round(getattr(pipeline, 'calibrated_threshold', BASE_THRESHOLD), 8),
        "total_transactions": getattr(pipeline, 'total_rows', 0) if pipeline else 0,
        "stream_queue_size": len(pipeline.stream_queue) if pipeline else 0,
        "uptime": round(time.time() - stats["start_time"], 1),
        "qiskit_available": QISKIT_AVAILABLE,
        "quantum_mode": quantum_backend_mode,
        "ibm_connected": ibm_manager.connected if ibm_manager else False,
    })


@app.route("/api/next", methods=["GET"])
def api_next():
    """Get next transaction, run through real model, return full analysis."""
    batch_size = int(request.args.get("batch", 1))
    batch_size = min(batch_size, 10)
    results = []

    for row in pipeline.get_next_batch(batch_size):
        pca_features = pipeline.transform(row)
        analysis = model.forward(pca_features, mode=quantum_backend_mode)

        # Dynamic threshold
        dyn_threshold = pipeline.get_dynamic_threshold()
        pipeline.recent_errors.append(analysis["reconError"])
        if len(pipeline.recent_errors) > 300:
            pipeline.recent_errors = pipeline.recent_errors[-300:]

        is_fraud = analysis["reconError"] > dyn_threshold
        ratio = analysis["reconError"] / dyn_threshold
        confidence = (
            min(99.9, 50 + 50 * (1 - 1 / (1 + math.exp(min(500, 3 * (ratio - 1))))))
            if is_fraud
            else min(99.9, 50 + 50 / (1 + math.exp(min(500, 3 * (ratio - 0.5)))))
        )
        risk_score = min(10, ratio * 5)

        stats["total_analyzed"] += 1
        if is_fraud:
            stats["total_fraud"] += 1

        results.append({
            "reconError": analysis["reconError"],
            "dynThreshold": round(dyn_threshold, 8),
            "isFraud": bool(is_fraud),
            "probs": analysis["probs"],
            "qState": analysis["qState"],
            "confidence": round(confidence, 1),
            "riskScore": round(risk_score, 1),
            "pcaFeatures": analysis["pcaFeatures"],
            "blochVec": analysis["blochVec"],
            "reconstructed": analysis["reconstructed"],
            "amount": float(row.get("Amount", 0)),
            "time": float(row.get("Time", 0)),
            "actualClass": int(row.get("Class", 0)),
            "totalAnalyzed": stats["total_analyzed"],
            "totalFraud": stats["total_fraud"],
        })

    return jsonify(results[0] if batch_size == 1 else results)


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """Predict on custom feature values (what-if simulation)."""
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Accept either raw features or named values
    if "features" in data:
        pca_features = np.array(data["features"], dtype=np.float32)[:PCA_COMPONENTS]
    else:
        # Build a row from named values
        row = {}
        for c in pipeline.feature_cols:
            if c in data:
                row[c] = float(data[c])
            else:
                row[c] = float(pipeline.scaler.mean_[pipeline.feature_cols.index(c)])
        pca_features = pipeline.transform(row)

    analysis = model.forward(pca_features, mode=quantum_backend_mode)
    dyn_threshold = pipeline.get_dynamic_threshold()
    is_fraud = analysis["reconError"] > dyn_threshold
    ratio = analysis["reconError"] / dyn_threshold

    return jsonify({
        "reconError": analysis["reconError"],
        "dynThreshold": round(dyn_threshold, 8),
        "isFraud": bool(is_fraud),
        "probs": analysis["probs"],
        "qState": analysis["qState"],
        "pcaFeatures": analysis["pcaFeatures"],
        "blochVec": analysis["blochVec"],
        "riskScore": round(min(10, ratio * 5), 1),
        "confidence": round(min(99.9, 50 + 50 * (1 - 1 / (1 + math.exp(min(500, 3 * (ratio - 1)))))), 1),
    })


@app.route("/api/metrics")
def api_metrics():
    """Return current system metrics."""
    return jsonify({
        "totalAnalyzed": stats["total_analyzed"],
        "totalFraud": stats["total_fraud"],
        "fraudRate": round(stats["total_fraud"] / max(1, stats["total_analyzed"]) * 100, 2),
        "dynamicThreshold": round(pipeline.get_dynamic_threshold(), 8),
        "baseThreshold": BASE_THRESHOLD,
        "recentErrorsMean": round(float(np.mean(pipeline.recent_errors)) if pipeline.recent_errors else 0, 8),
        "uptime": round(time.time() - stats["start_time"], 1),
        "pcaVariance": pipeline.pca.explained_variance_ratio_.tolist(),
    })


@app.route("/api/whatif", methods=["POST"])
def api_whatif():
    """What-if simulation: adjust Amount, V1, V14, V17 and see prediction."""
    data = request.json or {}
    row = {}
    for i, c in enumerate(pipeline.feature_cols):
        row[c] = float(pipeline.scaler.mean_[i])

    if "Amount" in data:
        row["Amount"] = float(data["Amount"])
    for key in ("V1", "V14", "V17"):
        if key in data:
            idx = pipeline.feature_cols.index(key)
            row[key] = float(pipeline.scaler.mean_[idx]) + float(data[key]) * float(pipeline.scaler.scale_[idx])

    pca_features = pipeline.transform(row)
    analysis = model.forward(pca_features, mode=quantum_backend_mode)
    dyn_threshold = pipeline.get_dynamic_threshold()
    is_fraud = analysis["reconError"] > dyn_threshold
    ratio = analysis["reconError"] / dyn_threshold

    return jsonify({
        "reconError": analysis["reconError"],
        "dynThreshold": round(dyn_threshold, 8),
        "isFraud": bool(is_fraud),
        "riskScore": round(min(10, ratio * 5), 1),
        "probs": analysis["probs"],
        "qState": analysis["qState"],
        "blochVec": analysis["blochVec"],
    })


# ─── IBM Quantum API Routes ──────────────────────────────────────────

@app.route("/api/ibm/status")
def api_ibm_status():
    """Report Qiskit availability and IBM connection status."""
    return jsonify({
        "qiskit_available": QISKIT_AVAILABLE,
        "connected": ibm_manager.connected if ibm_manager else False,
        "selected_backend": ibm_manager.selected_backend_name if ibm_manager else None,
        "available_backends": ibm_manager.available_backends if ibm_manager else [],
        "current_mode": quantum_backend_mode,
        "active_jobs": len([j for j in (ibm_manager.jobs.values() if ibm_manager else [])
                           if j['status'] in ('QUEUED', 'RUNNING')]),
    })


@app.route("/api/ibm/connect", methods=["POST"])
def api_ibm_connect():
    """Connect to IBM Quantum with API token."""
    if not QISKIT_AVAILABLE:
        return jsonify({"error": "Qiskit not installed"}), 400
    data = request.json
    token = data.get("token", "").strip()
    if not token:
        return jsonify({"error": "API token required"}), 400
    try:
        backends = ibm_manager.connect(token)
        return jsonify({"connected": True, "backends": backends})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/ibm/disconnect", methods=["POST"])
def api_ibm_disconnect():
    """Disconnect from IBM Quantum."""
    if ibm_manager:
        ibm_manager.disconnect()
    return jsonify({"connected": False})


@app.route("/api/ibm/select-backend", methods=["POST"])
def api_ibm_select_backend():
    """Select a specific IBM Quantum backend."""
    if not ibm_manager or not ibm_manager.connected:
        return jsonify({"error": "Not connected to IBM Quantum"}), 400
    data = request.json
    name = data.get("backend_name")
    if not name:
        return jsonify({"error": "backend_name required"}), 400
    try:
        info = ibm_manager.select_backend(name)
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/ibm/submit", methods=["POST"])
def api_ibm_submit():
    """Submit a transaction to IBM Quantum hardware (async)."""
    if not ibm_manager or not ibm_manager.connected:
        return jsonify({"error": "Not connected to IBM Quantum"}), 400
    if not ibm_manager.selected_backend:
        return jsonify({"error": "No backend selected"}), 400

    data = request.json or {}
    shots = data.get("shots", 4096)

    # Get PCA features
    if "features" in data:
        pca_features = np.array(data["features"], dtype=np.float32)
    else:
        rows = pipeline.get_next_batch(1)
        row = rows[0]
        pca_features = pipeline.transform(row)

    encoded = model.fc_in(pca_features)

    # Also run instant numpy result for comparison
    numpy_result = model.forward(pca_features)

    try:
        job_id = ibm_manager.submit_job(encoded, model.params, shots=shots)
        return jsonify({
            "job_id": job_id,
            "features": pca_features.tolist(),
            "encoded": encoded.tolist(),
            "numpy_result": numpy_result,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/ibm/job/<job_id>")
def api_ibm_job(job_id):
    """Get status and results of an IBM Quantum job."""
    if not ibm_manager:
        return jsonify({"error": "IBM Quantum not available"}), 400
    status = ibm_manager.get_job_status(job_id)
    if not status:
        return jsonify({"error": "Job not found"}), 404

    result = {"job": status}

    # If completed, compute full model output using hardware probabilities
    if status['status'] == 'DONE' and status['probs']:
        try:
            hw_probs = np.array(status['probs'], dtype=np.float32)
            x_hat = model.fc_out(hw_probs)
            with ibm_manager._lock:
                features = np.array(ibm_manager.jobs[job_id]['features'], dtype=np.float32)
            mse = float(np.mean((features - x_hat) ** 2))
            dyn_threshold = float(pipeline.get_dynamic_threshold())

            max_idx = int(np.argmax(hw_probs))
            q_state = "|" + format(max_idx, f"0{N_QUBITS}b") + "\u27E9"

            result['hardware_analysis'] = {
                'reconError': round(mse, 8),
                'dynThreshold': round(dyn_threshold, 8),
                'isFraud': bool(mse > dyn_threshold),
                'probs': status['probs'],
                'reconstructed': x_hat.tolist(),
                'qState': q_state,
            }
        except Exception as e:
            result['hardware_analysis_error'] = str(e)

    return jsonify(result)


@app.route("/api/ibm/jobs")
def api_ibm_jobs():
    """List all IBM Quantum jobs."""
    if not ibm_manager:
        return jsonify([])
    return jsonify(ibm_manager.get_all_jobs())


@app.route("/api/ibm/mode", methods=["POST"])
def api_ibm_mode():
    """Switch quantum execution mode."""
    global quantum_backend_mode
    data = request.json
    mode = data.get("mode", "numpy")
    if mode not in ("numpy", "aer_statevector", "aer_sampler"):
        return jsonify({"error": f"Invalid mode: {mode}"}), 400
    if mode.startswith("aer") and not QISKIT_AVAILABLE:
        return jsonify({"error": "Qiskit not installed — cannot use Aer"}), 400
    quantum_backend_mode = mode
    return jsonify({"mode": quantum_backend_mode})


@app.route("/api/ibm/validate", methods=["POST"])
def api_ibm_validate():
    """Validate numpy vs Qiskit Aer equivalence."""
    if not QISKIT_AVAILABLE:
        return jsonify({"error": "Qiskit not installed"}), 400

    # Sample transaction
    rows = pipeline.get_next_batch(1)
    row = rows[0]
    pca_features = pipeline.transform(row)
    pipeline.stream_index = max(0, pipeline.stream_index - 1)

    # Numpy result
    numpy_result = model.forward(pca_features, mode='numpy')
    numpy_probs = numpy_result['probs']

    # Aer statevector result
    encoded = model.fc_in(pca_features.astype(np.float32))
    aer_probs = run_aer_statevector(encoded, model.params)

    # Compare
    diff = np.abs(np.array(numpy_probs) - aer_probs)
    max_diff = float(np.max(diff))
    mean_diff = float(np.mean(diff))
    is_equivalent = max_diff < 1e-4

    return jsonify({
        "equivalent": is_equivalent,
        "max_diff": max_diff,
        "mean_diff": mean_diff,
        "numpy_probs": numpy_probs,
        "aer_probs": aer_probs.tolist(),
    })


# ─── Initialization (runs for both gunicorn and direct execution) ────
initialize()

# ─── Entry Point ─────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
