# 🔮 Quantum Eye

## Quantum Digital Twin for Real-Time Credit Card Fraud Detection

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Qiskit](https://img.shields.io/badge/Qiskit-2.2.1-purple.svg)](https://qiskit.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Overview

**Quantum Eye** is a groundbreaking fraud detection system that combines **Variational Quantum Autoencoders (VQAE)** with **Digital Twin Technology** to create a living, evolving replica of financial transaction behavior. This unique hybrid approach enables real-time anomaly detection with unprecedented accuracy and adaptability.

### 🎯 What Makes Quantum Eye Unique?

| Feature | Traditional Systems | Quantum Eye |
|---------|-------------------|-------------|
| **Architecture** | Static ML models | **Quantum Digital Twin** — constantly synchronized with real-world data |
| **Detection** | Rule-based or classical ML | **Quantum Neural Network** — exploits quantum superposition & entanglement |
| **Adaptability** | Periodic retraining | **Real-time feedback learning** — adapts to evolving fraud patterns |
| **Simulation** | Limited what-if analysis | **Full what-if simulation** — test scenarios before deployment |
| **Accuracy** | 70-85% typical | **89.16%** with continuous improvement |

---

## 🔄 Digital Twin Architecture

Quantum Eye implements a **true Digital Twin** — not just a model, but a living replica of the financial transaction ecosystem:

```
                    ┌─────────────────────────────────────────┐
                    │         QUANTUM DIGITAL TWIN            │
                    │                                         │
   Real-World       │  ┌─────────────────────────────────┐   │
   Transactions ───▶│  │     Real-Time Synchronization   │   │
                    │  │   • Continuous data ingestion    │   │
                    │  │   • Dynamic threshold adaptation │   │
                    │  │   • Pattern drift detection      │   │
                    │  └─────────────┬───────────────────┘   │
                    │                │                        │
                    │  ┌─────────────▼───────────────────┐   │
                    │  │      Quantum VQAE Core          │   │
                    │  │   • 4-qubit variational circuit │   │
                    │  │   • 10 entanglement layers      │   │
                    │  │   • Anomaly reconstruction      │   │
                    │  └─────────────┬───────────────────┘   │
                    │                │                        │
                    │  ┌─────────────▼───────────────────┐   │
   Predictions  ◀───│  │      What-If Simulation         │   │
   & Insights       │  │   • Test fraud scenarios        │   │
                    │  │   • Tune detection parameters   │   │
                    │  │   • Predict before deploy       │   │
                    │  └─────────────┬───────────────────┘   │
                    │                │                        │
                    │  ┌─────────────▼───────────────────┐   │
                    │  │      Feedback Learning          │   │
   Analyst      ───▶│  │   • Human-in-the-loop review   │   │
   Feedback         │  │   • Continuous model refinement │   │
                    │  │   • Adaptive threshold tuning   │   │
                    │  └─────────────────────────────────┘   │
                    │                                         │
                    └─────────────────────────────────────────┘
```

### 🌐 Digital Twin Components

1. **Real-Time Synchronization**
   - Continuously ingests transaction streams
   - Dynamically adapts detection thresholds based on recent patterns
   - Detects concept drift and fraud pattern evolution

2. **Quantum VQAE Core**
   - 4-qubit variational quantum circuit with 10 layers
   - Quantum superposition enables parallel pattern exploration
   - Entanglement captures complex correlations classical systems miss

3. **What-If Simulation Engine**
   - Test hypothetical transactions before real-world deployment
   - Tune parameters in a safe sandbox environment
   - Predict system behavior under different scenarios

4. **Feedback Learning Loop**
   - Incorporates analyst decisions into model refinement
   - Continuous learning without full retraining
   - Maintains accuracy as fraud tactics evolve

---

## 🚀 Key Features

- 🧠 **Quantum Neural Network** — 4-qubit, 10-layer variational circuit with 120 trainable parameters
- 🔄 **Digital Twin Sync** — Real-time synchronization with transaction streams
- ⚡ **Real-time Detection** — ~50ms inference with dynamic threshold adaptation
- 🎯 **89.16% Accuracy** — Superior detection with 91%+ F1 score
- 🔮 **What-If Simulation** — Test scenarios before deployment
- 📈 **Feedback Learning** — Continuous improvement from analyst input
- 🖥️ **Interactive Dashboard** — 3D Bloch sphere visualization, live metrics
- 🔗 **IBM Quantum Ready** — Connect to real quantum hardware

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Quantum Eye System                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │   Raw Data   │───▶│  PCA (4-dim) │───▶│   fc_in      │   │
│  │  (30 feat)   │    │   Scaler     │    │   (4→4)      │   │
│  └──────────────┘    └──────────────┘    └──────┬───────┘   │
│                                                  │           │
│                      ┌───────────────────────────▼────────┐  │
│                      │     Quantum Circuit (4q, 10L)      │  │
│                      │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │  │
│                      │  │ RY  │ │ RX  │ │ RY  │ │ RZ  │   │  │
│                      │  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘   │  │
│                      │     └───CNOT Ring Entanglement───┘   │  │
│                      └───────────────────────────┬────────┘  │
│                                                  │           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────▼───────┐   │
│  │   Anomaly    │◀───│   fc_out     │◀───│  Measure     │   │
│  │   Score      │    │   (16→4)     │    │  (16 probs)  │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yashas396/QuantumEye.git
cd QuantumEye

# Install dependencies
pip install -r requirements.txt

# Decompress data (if needed)
python build.py

# Run the server
python app.py
```

### Access the Dashboard

Open your browser and navigate to:
```
http://localhost:5000
```

---

## 📁 Project Structure

```
QuantumEye/
├── app.py                  # Flask backend with Digital Twin logic
├── interface.html          # Interactive dashboard UI
├── qiskit_backend.py       # Qiskit quantum circuit implementation
├── qdt_fraud_model/        # Pre-trained VQAE model weights
├── creditcard.csv.gz       # Compressed training dataset
├── build.py                # Build script for deployment
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config
├── railway.toml            # Railway deployment config
└── Procfile                # Heroku-style process file
```

---

## 🔬 How It Works

### 1. **Data Preprocessing**
- Transactions are scaled to [-1, 1] range
- PCA reduces 30 features to 4 quantum-compatible dimensions

### 2. **Quantum Encoding**
- 4 features are encoded into 4 qubits using RY rotation gates
- Angle embedding: `RY(feature_value)`

### 3. **Variational Layers**
- 10 layers of parametrized rotations (RX, RY, RZ)
- CNOT ring entanglement between adjacent qubits
- 120 trainable parameters

### 4. **Anomaly Detection via Digital Twin**
- Reconstruction error (MSE) measures transaction normality
- Digital Twin maintains dynamic baseline of "normal" behavior
- High error = anomaly = potential fraud
- Threshold adapts in real-time based on recent transaction patterns

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard interface |
| `/api/status` | GET | System status and metrics |
| `/api/next` | GET | Analyze next transaction |
| `/api/predict` | POST | Custom transaction prediction |
| `/api/whatif` | POST | **Digital Twin what-if simulation** |
| `/api/metrics` | GET | Current system metrics |
| `/api/ibm/status` | GET | IBM Quantum connection status |
| `/api/ibm/connect` | POST | Connect to IBM Quantum |

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Accuracy** | **89.16%** |
| **F1-Score** | 91.23% |
| Qubits | 4 |
| Layers | 10 |
| Parameters | 120 |
| Inference Time | ~50ms |

---

## 🚀 Deployment

### Render
```bash
# Automatic deployment via render.yaml
# Visit: https://quantumeye-aqvh.onrender.com
```

### Railway
```bash
# Automatic deployment via railway.toml
# Uses Nixpacks builder
```

### Local with Gunicorn
```bash
gunicorn app:app --bind 0.0.0.0:5000 --timeout 120 --workers 1
```

---

## 🔗 IBM Quantum Integration

Connect to real IBM Quantum hardware:

1. Get your API token from [IBM Quantum](https://quantum.ibm.com/)
2. In the dashboard, click "IBM Quantum" tab
3. Enter your API token
4. Select a backend (e.g., `ibm_brisbane`)
5. Submit transactions for hardware execution

---

## 📚 Documentation

- [Detailed Documentation](QuantumEye_Detailed_Documentation.md)
- [Code Explanation](QuantumEye_Code_Explanation.md)
- [UI/UX Framework](UI_UX_FRAMEWORK.md)

---

## 🛠️ Technology Stack

- **Backend**: Flask, Gunicorn
- **Quantum**: Qiskit, Qiskit Aer, IBM Quantum Runtime
- **ML**: PyTorch, Scikit-learn, NumPy, Pandas
- **Frontend**: HTML5, CSS3, JavaScript, Three.js
- **Architecture**: Digital Twin, VQAE, Real-time Streaming

---

## 👥 Team TATTVA

Built with ❤️ by **Team TATTVA** for quantum-enhanced financial security.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Qiskit Team](https://qiskit.org/) for quantum computing framework
- [IBM Quantum](https://quantum.ibm.com/) for cloud quantum access
- Credit card fraud dataset from [Kaggle](https://www.kaggle.com/mlg-ulb/creditcardfraud)
