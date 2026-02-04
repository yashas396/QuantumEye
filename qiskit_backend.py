"""
QuantumEye v2.0 - Qiskit Backend Integration
Provides: circuit builder, Aer simulation, IBM Quantum hardware manager.

Circuit matches the numpy VQAE implementation in app.py exactly:
  4 qubits, RY angle embedding, 10 variational layers (RX,RY,RZ + CNOT ring)
"""

import numpy as np
import threading
import time
import uuid
from datetime import datetime

from qiskit.circuit import QuantumCircuit

N_QUBITS = 4
N_LAYERS = 10
N_STATES = 2 ** N_QUBITS  # 16


# ─── Circuit Builders ────────────────────────────────────────────────

def build_vqae_circuit(features, params):
    """
    Build a Qiskit QuantumCircuit matching the numpy VQAE exactly.

    Args:
        features: array shape (4,) - output of fc_in
        params:   array shape (10, 4, 3) - variational circuit parameters

    Returns:
        QuantumCircuit with 4 qubits, no measurements (for statevector)
    """
    qc = QuantumCircuit(N_QUBITS)

    # Angle embedding: RY(feature[q]) on qubit q
    for q in range(N_QUBITS):
        qc.ry(float(features[q]), q)

    # 10 variational layers
    for layer in range(N_LAYERS):
        # Per-qubit rotations: RX, RY, RZ
        for q in range(N_QUBITS):
            qc.rx(float(params[layer, q, 0]), q)
            qc.ry(float(params[layer, q, 1]), q)
            qc.rz(float(params[layer, q, 2]), q)

        # CNOT ring: (0→1), (1→2), (2→3), (3→0)
        for q in range(N_QUBITS):
            qc.cx(q, (q + 1) % N_QUBITS)

    return qc


def build_vqae_circuit_measured(features, params):
    """Same circuit with measurement gates appended (for sampler/hardware)."""
    qc = build_vqae_circuit(features, params)
    qc.measure_all()
    return qc


# ─── Aer Execution ──────────────────────────────────────────────────

def run_aer_statevector(features, params):
    """
    Run circuit on Aer StatevectorSimulator (exact, no shot noise).
    Returns: np.array shape (16,) — probabilities matching numpy sim.
    """
    from qiskit_aer import AerSimulator

    qc = build_vqae_circuit(features, params)
    qc.save_statevector()

    sim = AerSimulator(method='statevector')
    result = sim.run(qc).result()
    sv = result.get_statevector()

    # Qiskit statevector is indexed by integer state (0..15)
    # but uses LITTLE-ENDIAN qubit ordering internally.
    # We need to reverse to match our big-endian numpy convention.
    sv_array = np.array(sv)
    probs_raw = np.abs(sv_array) ** 2

    # Reverse qubit ordering: swap bit positions to match numpy convention
    probs = np.zeros(N_STATES, dtype=np.float32)
    for i in range(N_STATES):
        # Reverse the bit order: e.g. for 4 qubits, 0b0001 → 0b1000
        reversed_idx = int(format(i, f'0{N_QUBITS}b')[::-1], 2)
        probs[reversed_idx] = probs_raw[i]

    probs = probs / probs.sum()
    return probs


def run_aer_sampler(features, params, shots=8192):
    """
    Run circuit on Aer with shot-based sampling.
    Returns: np.array shape (16,) — estimated probabilities.
    """
    from qiskit_aer import AerSimulator

    qc = build_vqae_circuit_measured(features, params)
    sim = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()

    probs = np.zeros(N_STATES, dtype=np.float32)
    for bitstring, count in counts.items():
        # Qiskit bitstrings are little-endian; reverse to match our big-endian
        idx = int(bitstring[::-1], 2)
        probs[idx] = count / shots

    return probs


# ─── IBM Quantum Hardware Manager ───────────────────────────────────

class IBMQuantumManager:
    """Manages IBM Quantum connection, job submission, polling, and results."""

    def __init__(self):
        self.service = None
        self.connected = False
        self.api_token = None
        self.available_backends = []
        self.selected_backend = None
        self.selected_backend_name = None
        self.jobs = {}
        self._lock = threading.Lock()
        self._poll_thread = None
        self._polling = False

    def connect(self, api_token):
        """Connect to IBM Quantum Platform."""
        from qiskit_ibm_runtime import QiskitRuntimeService

        self.api_token = api_token

        # Try ibm_quantum_platform first, then ibm_cloud
        last_err = None
        for channel in ('ibm_quantum_platform', 'ibm_cloud'):
            try:
                self.service = QiskitRuntimeService(
                    channel=channel,
                    token=api_token,
                )
                self.connected = True
                break
            except Exception as e:
                last_err = e
                continue
        else:
            raise last_err or RuntimeError("Could not connect to IBM Quantum")

        # Enumerate backends
        backends = self.service.backends()
        self.available_backends = []
        for b in backends:
            try:
                # Modern qiskit-ibm-runtime API
                name = getattr(b, 'name', None) or getattr(b.configuration(), 'backend_name', str(b))
                n_qubits = getattr(b, 'num_qubits', None)
                if n_qubits is None:
                    try:
                        n_qubits = b.configuration().n_qubits
                    except Exception:
                        n_qubits = 0
                is_sim = getattr(b, 'simulator', False)
                if not isinstance(is_sim, bool):
                    try:
                        is_sim = b.configuration().simulator
                    except Exception:
                        is_sim = False
                try:
                    st = b.status()
                    status_msg = getattr(st, 'status_msg', str(st))
                    pending = getattr(st, 'pending_jobs', 0)
                except Exception:
                    status_msg = 'unknown'
                    pending = 0
                self.available_backends.append({
                    'name': name,
                    'n_qubits': n_qubits,
                    'simulator': is_sim,
                    'status': status_msg,
                    'pending_jobs': pending,
                })
            except Exception:
                continue

        return self.available_backends

    def disconnect(self):
        """Disconnect from IBM Quantum."""
        self._polling = False
        self.service = None
        self.connected = False
        self.api_token = None
        self.available_backends = []
        self.selected_backend = None
        self.selected_backend_name = None

    def select_backend(self, backend_name):
        """Select a specific IBM backend by name."""
        if not self.connected:
            raise RuntimeError("Not connected to IBM Quantum")
        self.selected_backend = self.service.backend(backend_name)
        self.selected_backend_name = backend_name
        n_qubits = getattr(self.selected_backend, 'num_qubits', None)
        if n_qubits is None:
            try:
                n_qubits = self.selected_backend.configuration().n_qubits
            except Exception:
                n_qubits = 0
        try:
            st = self.selected_backend.status()
            status_msg = getattr(st, 'status_msg', str(st))
            pending = getattr(st, 'pending_jobs', 0)
        except Exception:
            status_msg = 'available'
            pending = 0
        return {
            'name': backend_name,
            'n_qubits': n_qubits,
            'status': status_msg,
            'pending_jobs': pending,
        }

    def submit_job(self, features, params, shots=4096):
        """
        Submit a VQAE circuit to IBM Quantum hardware.
        Returns a local job_id for tracking.
        """
        from qiskit_ibm_runtime import SamplerV2 as Sampler
        from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

        if not self.selected_backend:
            raise RuntimeError("No backend selected")

        # Build and transpile
        qc = build_vqae_circuit_measured(features, params)
        pm = generate_preset_pass_manager(
            optimization_level=1,
            backend=self.selected_backend
        )
        transpiled = pm.run(qc)

        # Submit via Sampler primitive (v0.45+: use mode= instead of backend=)
        sampler = Sampler(mode=self.selected_backend)
        job = sampler.run([transpiled], shots=shots)

        job_id = str(uuid.uuid4())[:8]
        with self._lock:
            self.jobs[job_id] = {
                'ibm_job_id': job.job_id(),
                'ibm_job': job,
                'status': 'QUEUED',
                'submitted_at': datetime.now().isoformat(),
                'completed_at': None,
                'features': features.tolist(),
                'backend': self.selected_backend_name,
                'shots': shots,
                'probs': None,
                'error': None,
            }

        # Start polling if not already running
        if not self._polling:
            self._start_polling()

        return job_id

    def _start_polling(self):
        self._polling = True
        self._poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._poll_thread.start()

    def _poll_loop(self):
        while self._polling:
            with self._lock:
                active = [jid for jid, j in self.jobs.items()
                          if j['status'] in ('QUEUED', 'RUNNING')]

            if not active:
                self._polling = False
                return

            for job_id in active:
                try:
                    with self._lock:
                        ibm_job = self.jobs[job_id]['ibm_job']

                    status = ibm_job.status()
                    status_name = status.name if hasattr(status, 'name') else str(status)

                    if status_name == 'DONE':
                        self._process_result(job_id)
                    elif status_name in ('CANCELLED', 'ERROR'):
                        with self._lock:
                            self.jobs[job_id]['status'] = status_name
                            try:
                                self.jobs[job_id]['error'] = str(ibm_job.error_message())
                            except Exception:
                                self.jobs[job_id]['error'] = f"Job {status_name}"
                    else:
                        with self._lock:
                            self.jobs[job_id]['status'] = status_name

                except Exception as e:
                    with self._lock:
                        self.jobs[job_id]['error'] = str(e)

            time.sleep(10)

    def _process_result(self, job_id):
        """Extract probabilities from completed IBM job."""
        with self._lock:
            job_info = self.jobs[job_id]
            ibm_job = job_info['ibm_job']

        result = ibm_job.result()

        try:
            # SamplerV2 result format
            pub_result = result[0]
            counts = pub_result.data.meas.get_counts()
        except Exception:
            # Fallback for older result formats
            counts = result.get_counts()

        shots = job_info['shots']
        probs = np.zeros(N_STATES, dtype=np.float32)
        for bitstring, count in counts.items():
            # Reverse bitstring: Qiskit little-endian → our big-endian
            idx = int(bitstring[::-1], 2)
            probs[idx] = count / shots

        with self._lock:
            job_info['probs'] = probs.tolist()
            job_info['status'] = 'DONE'
            job_info['completed_at'] = datetime.now().isoformat()

    def get_job_status(self, job_id):
        """Get status of a specific job."""
        with self._lock:
            if job_id not in self.jobs:
                return None
            j = self.jobs[job_id]
            return {
                'job_id': job_id,
                'ibm_job_id': j['ibm_job_id'],
                'status': j['status'],
                'backend': j['backend'],
                'shots': j['shots'],
                'submitted_at': j['submitted_at'],
                'completed_at': j.get('completed_at'),
                'probs': j['probs'],
                'error': j['error'],
            }

    def get_all_jobs(self):
        """Get status of all jobs."""
        with self._lock:
            job_ids = list(self.jobs.keys())
        return [self.get_job_status(jid) for jid in job_ids]
