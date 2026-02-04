# 🔮 QuantumEye AQVH

## Quantum-Enhanced Credit Card Fraud Detection System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Qiskit](https://img.shields.io/badge/Qiskit-2.2.1-purple.svg)](https://qiskit.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Overview

**QuantumEye AQVH** is a cutting-edge fraud detection system that leverages **Variational Quantum Autoencoders (VQAE)** to detect anomalous credit card transactions in real-time. By combining quantum computing principles with classical machine learning, it achieves superior detection of fraudulent patterns that traditional systems miss.

### Key Features

- 🧠 **Quantum Neural Network** — 4-qubit, 10-layer variational circuit
- ⚡ **Real-time Detection** — Streaming transaction analysis with dynamic thresholds  
- 🎯 **High Accuracy** — 88%+ accuracy, 91%+ F1 score on fraud detection
- 🔄 **Digital Twin Architecture** — What-if simulation and feedback learning
- 🖥️ **Interactive Dashboard** — Real-time visualization with 3D Bloch sphere
- 🔗 **IBM Quantum Ready** — Connect to real quantum hardware

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    QuantumEye AQVH System                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Raw Data   │───▶│  PCA (4-dim) │───▶│   fc_in      │  │
│  │  (30 feat)   │    │   Scaler     │    │   (4→4)      │  │
│  └──────────────┘    └──────────────┘    └──────┬───────┘  │
│                                                  │          │
│                      ┌───────────────────────────▼────────┐ │
│                      │     Quantum Circuit (4q, 10L)      │ │
│                      │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │ │
│                      │  │ RY  │ │ RX  │ │ RY  │ │ RZ  │  │ │
│                      │  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘  │ │
│                      │     └───CNOT Ring Entanglement───┘  │ │
│                      └───────────────────────────┬────────┘ │
│                                                  │          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────▼───────┐  │
│  │   Anomaly    │◀───│   fc_out     │◀───│  Measure     │  │
│  │   Score      │    │   (16→4)     │    │  (16 probs)  │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                             │
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
├── app.py                  # Flask backend with quantum model
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

### 4. **Anomaly Detection**
- Reconstruction error (MSE) measures transaction normality
- High error = anomaly = potential fraud
- Dynamic threshold adapts to transaction patterns

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard interface |
| `/api/status` | GET | System status and metrics |
| `/api/next` | GET | Analyze next transaction |
| `/api/predict` | POST | Custom transaction prediction |
| `/api/whatif` | POST | What-if simulation |
| `/api/metrics` | GET | Current system metrics |
| `/api/ibm/status` | GET | IBM Quantum connection status |
| `/api/ibm/connect` | POST | Connect to IBM Quantum |

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Accuracy | 88.44% |
| F1-Score | 91.23% |
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

---

## 👥 Team AQVH

Built with ❤️ for quantum-enhanced financial security.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Qiskit Team](https://qiskit.org/) for quantum computing framework
- [IBM Quantum](https://quantum.ibm.com/) for cloud quantum access
- Credit card fraud dataset from [Kaggle](https://www.kaggle.com/mlg-ulb/creditcardfraud)
