# ⚛️ QuantumEye v2.0 - UI/UX Framework

## Quantum Digital Twin Fraud Detection System

---

## 1. Project Overview

| Attribute | Value |
|-----------|-------|
| **Project Name** | QuantumEye - Quantum Fraud Detection System |
| **Core Technology** | Variational Quantum Autoencoder (VQAE) |
| **Data Source** | Real-time credit card transaction data |
| **Model** | Quantum Digital Twin (qdt_fraud_model) |
| **Principle** | Reconstruction-based anomaly detection |

### System Architecture
```
creditcard.csv → Python Backend → VQAE Model → API → Frontend Dashboard
                     ↓
              Real-time predictions with quantum state visualization
```

---

## 2. Design System

### 2.1 Color Palette

```css
/* Quantum Theme Colors */
--quantum-primary: #00ffff;      /* Cyan - Quantum superposition */
--quantum-secondary: #0080ff;    /* Blue - Stable state */
--quantum-tertiary: #667eea;     /* Purple - Entanglement */

/* Status Colors */
--status-safe: #00d2d3;          /* Normal transaction */
--status-warning: #ffa502;       /* Medium risk */
--status-fraud: #ff4757;         /* Fraud detected */

/* Background */
--bg-deep: #0a0e27;              /* Deep space */
--bg-surface: #1a1f3a;           /* Surface */
--bg-panel: rgba(20, 25, 45, 0.8);

/* Text */
--text-primary: #ffffff;
--text-secondary: #8892b0;
```

### 2.2 Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Score Display | Segoe UI | 48px | 700 |
| Metric Values | Monospace | 24px | 700 |
| Panel Headers | Segoe UI | 12px | 500 |
| Body Text | Segoe UI | 14px | 400 |
| Quantum States | Monospace | 18px | 600 |

---

## 3. Quantum Visual Elements

### 3.1 Quantum State Notation
Display quantum states in Dirac notation:
- `|0000⟩` - 4-qubit ground state
- `|ψ⟩ = α|0⟩ + β|1⟩` - Superposition state

### 3.2 Quantum Animations

**1. Superposition Wave**
```css
@keyframes quantumWave {
    0% { transform: translateX(0) scaleY(1); }
    50% { transform: translateX(10px) scaleY(1.2); }
    100% { transform: translateX(0) scaleY(1); }
}
```

**2. Entanglement Pulse**
```css
@keyframes entanglementPulse {
    0%, 100% { box-shadow: 0 0 5px var(--quantum-primary); }
    50% { box-shadow: 0 0 30px var(--quantum-primary), 0 0 60px var(--quantum-secondary); }
}
```

**3. Qubit Rotation**
```css
@keyframes qubitRotate {
    0% { transform: rotateY(0deg) rotateX(0deg); }
    100% { transform: rotateY(360deg) rotateX(360deg); }
}
```

**4. Probability Collapse**
```css
@keyframes probabilityCollapse {
    0% { opacity: 0.3; transform: scale(1.5); }
    100% { opacity: 1; transform: scale(1); }
}
```

---

## 4. Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  ⚛️ QUANTUMEYE v2.0               ● Live    🔔 Alerts    ⚙️ Config │
├──────────────┬────────────────────────────────────┬─────────────────┤
│              │                                    │                 │
│  THREAT      │    QUANTUM RECONSTRUCTION          │  DEEP SCAN      │
│  MATRIX      │    VISUALIZATION                   │  ANALYSIS       │
│              │                                    │                 │
│  ┌─────────┐ │  ┌──────────────────────────────┐ │ ┌─────────────┐ │
│  │Card 4521│ │  │                              │ │ │   95.2%     │ │
│  │ $2,450  │ │  │     3D Bloch Sphere          │ │ │  ANOMALY    │ │
│  │ 8.5/10  │ │  │     Visualization            │ │ │   SCORE     │ │
│  ├─────────┤ │  │                              │ │ ├─────────────┤ │
│  │Card 3892│ │  │     [Rotating quantum        │ │ │ Error:0.024 │ │
│  │ $890    │ │  │      state vectors]          │ │ │ Thresh:0.015│ │
│  │ 6.2/10  │ │  │                              │ │ │ State:|0011⟩│ │
│  ├─────────┤ │  └──────────────────────────────┘ │ │ Conf: 98.7% │ │
│  │Card 7234│ │                                   │ ├─────────────┤ │
│  │ $5,670  │ │  ┌──────────────────────────────┐ │ │ RISK FACTORS│ │
│  │ 9.1/10  │ │  │  Reconstruction Waveform     │ │ │ ● Behavior  │ │
│  └─────────┘ │  │  ≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋   │ │ │ ● Location  │ │
│              │  └──────────────────────────────┘ │ │ ● Device    │ │
│              │                                   │ └─────────────┘ │
│              │  [Simulate] [Verify] [Configure]  │                 │
└──────────────┴───────────────────────────────────┴─────────────────┘
```

---

## 5. Component Specifications

### 5.1 Threat Matrix Panel
- Displays real-time transactions from `creditcard.csv`
- Color-coded risk levels (cyan/orange/red borders)
- Click to expand transaction details
- Auto-refresh every 1 second

### 5.2 Quantum Reconstruction Visualization
- **3D Bloch Sphere** showing quantum state
- **Original vs Reconstructed** data lines
- **Anomaly Points** highlighted in orange
- Interactive rotation with mouse

### 5.3 Anomaly Score Gauge
- Circular SVG gauge (0-100%)
- Animated fill based on VQAE reconstruction error
- Formula: `Score = (1 - sigmoid(error/threshold)) × 100`

### 5.4 Metrics Grid

| Metric | Source | Update Rate |
|--------|--------|-------------|
| Reconstruction Error | VQAE model output | Real-time |
| Threshold | Adaptive calculation | Per-batch |
| Quantum State | Circuit measurement | Per-transaction |
| Confidence | Model probability | Real-time |

---

## 6. Real-Time Data Integration

### 6.1 Backend API Endpoints

```python
# Flask/FastAPI Backend
GET  /api/transactions      # Stream transactions
POST /api/predict           # Single prediction
GET  /api/metrics           # Model metrics
POST /api/simulate          # What-if simulation
WS   /ws/live               # WebSocket for real-time
```

### 6.2 Data Flow

```
1. Load creditcard.csv → Pandas DataFrame
2. Preprocess features (V1-V28, Amount, Time)
3. Feed to VQAE model (qdt_fraud_model)
4. Calculate reconstruction error
5. Compare with adaptive threshold
6. Return: {is_fraud, score, quantum_state, confidence}
7. Stream to frontend via WebSocket
```

### 6.3 Model Integration

```python
# Load trained model
model = torch.load('qdt_fraud_model/data.pkl')
model.eval()

# Predict
def predict(transaction):
    input_tensor = preprocess(transaction)
    reconstructed = model(input_tensor)
    error = F.mse_loss(input_tensor, reconstructed)
    is_fraud = error > threshold
    return {'fraud': is_fraud, 'error': error.item()}
```

---

## 7. Interactive Features

### 7.1 Transaction Detail Modal
- Click any threat item → Opens detailed analysis
- Shows: Card ID, Amount, Location, Time
- Displays: Reconstruction analysis, quantum state
- Actions: Block, Verify, Flag for Review

### 7.2 Simulate Attack Button
```javascript
function simulateAttack() {
    // Inject synthetic fraud pattern
    // Visualize detection in real-time
    // Show quantum state collapse animation
}
```

### 7.3 What-If Simulation
- Adjust transaction parameters
- See predicted fraud probability
- Visualize decision boundary

---

## 8. Quantum Visualization Standards

### 8.1 Bloch Sphere Representation
- X-axis: Real component
- Y-axis: Imaginary component
- Z-axis: Probability amplitude
- Sphere surface: Pure states
- Interior: Mixed states

### 8.2 Circuit Diagram Display
```
q₀: ─[H]─●───[RY(θ)]─
         │
q₁: ─────X───[RZ(φ)]─
```

### 8.3 Probability Distribution
- Bar chart showing measurement probabilities
- States |00⟩, |01⟩, |10⟩, |11⟩
- Animated collapse on measurement

---

## 9. Responsive Breakpoints

| Breakpoint | Layout | Columns |
|------------|--------|---------|
| ≥1440px | Full 3-column | 350px \| 1fr \| 400px |
| 1024-1439px | Standard | 300px \| 1fr \| 350px |
| 768-1023px | Tablet | 2-column stack |
| <768px | Mobile | Single column |

---

## 10. Accessibility & Standards

### 10.1 WCAG 2.1 Compliance
- ✅ Color contrast ratio ≥ 4.5:1
- ✅ Keyboard navigation support
- ✅ Screen reader labels (ARIA)
- ✅ Focus indicators

### 10.2 Performance Targets
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3s
- 3D render: 60fps
- API response: < 200ms

---

## 11. Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, CSS3, JavaScript |
| 3D Graphics | Three.js |
| Charts | Chart.js / D3.js |
| Backend | Python (Flask/FastAPI) |
| ML Framework | PyTorch + Qiskit |
| Data | Pandas, NumPy |
| Real-time | WebSocket |

---

## 12. File Structure

```
QuantumEye/
├── frontend/
│   ├── index.html          # Main dashboard
│   ├── css/
│   │   └── quantum-theme.css
│   └── js/
│       ├── quantum-viz.js   # 3D visualizations
│       ├── api-client.js    # Backend connection
│       └── realtime.js      # WebSocket handler
├── backend/
│   ├── app.py               # Flask/FastAPI server
│   ├── model_loader.py      # Load VQAE model
│   └── predictor.py         # Inference logic
├── data/
│   └── creditcard.csv       # Transaction data
├── models/
│   └── qdt_fraud_model/     # Trained model
└── docs/
    └── UI_UX_Framework.md   # This document
```

---

## 13. Implementation Checklist

- [ ] Backend API with model integration
- [ ] WebSocket for real-time streaming
- [ ] 3D Bloch sphere visualization
- [ ] Quantum state animations
- [ ] Responsive CSS implementation
- [ ] Accessibility compliance
- [ ] Error handling & fallbacks
- [ ] Performance optimization
- [ ] Testing & validation

---

*Document Version: 2.0 | Last Updated: February 2026*
*QuantumEye - Securing Transactions with Quantum Intelligence*
