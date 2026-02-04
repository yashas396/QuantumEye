# 🎨 QuantumEye v2.0 - UI/UX Framework

## Quantum Fraud Detection System - Design System & User Experience Guide

---

## 📋 Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Color System](#2-color-system)
3. [Typography](#3-typography)
4. [Component Library](#4-component-library)
5. [Layout System](#5-layout-system)
6. [User Personas](#6-user-personas)
7. [User Flows](#7-user-flows)
8. [Page Structure](#8-page-structure)
9. [Interaction Patterns](#9-interaction-patterns)
10. [Accessibility Guidelines](#10-accessibility-guidelines)
11. [Responsive Design](#11-responsive-design)
12. [Animation & Motion](#12-animation--motion)

---

## 1. Design Philosophy

### 1.1 Core Principles

| Principle | Description |
|-----------|-------------|
| **Quantum Aesthetic** | Futuristic, dark-mode interface reflecting quantum computing's cutting-edge nature |
| **Data-First** | Every pixel serves to communicate fraud detection insights |
| **Real-Time Focus** | Emphasize live monitoring with animated indicators |
| **Trust & Security** | Visual language that conveys reliability and protection |
| **Actionable Intelligence** | Clear paths from detection to decision |

### 1.2 Visual Identity

```
┌─────────────────────────────────────────────────────────────┐
│                    QUANTUMEYE BRAND                         │
├─────────────────────────────────────────────────────────────┤
│  Theme:     Cyberpunk / Futuristic / Scientific             │
│  Mood:      Professional, Trustworthy, High-Tech            │
│  Style:     Glassmorphism + Neon Accents                    │
│  Feel:      Command Center / Mission Control                │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Design Metaphors

- **Quantum States**: Use wave patterns and superposition visuals
- **Digital Twin**: Mirror/reflection imagery
- **Shield/Protection**: Security-focused iconography
- **Neural Networks**: Connected node visualizations

---

## 2. Color System

### 2.1 Primary Palette

```css
:root {
    /* Background Colors */
    --bg-primary: #0a0e27;      /* Deep Space Blue */
    --bg-secondary: #1a1f3a;    /* Midnight Blue */
    --bg-tertiary: #2d3561;     /* Slate Blue */
    --bg-panel: rgba(20, 25, 45, 0.8);
    
    /* Accent Colors */
    --accent-cyan: #00ffff;     /* Primary Accent - Quantum */
    --accent-blue: #0080ff;     /* Secondary Accent */
    --accent-purple: #667eea;   /* Tertiary Accent */
    --accent-magenta: #ff00ff;  /* Highlight */
    
    /* Status Colors */
    --status-success: #00d2d3;  /* Safe/Normal */
    --status-warning: #ffa502;  /* Medium Risk */
    --status-danger: #ff4757;   /* High Risk/Fraud */
    --status-info: #64b5f6;     /* Information */
    
    /* Text Colors */
    --text-primary: #ffffff;
    --text-secondary: #8892b0;
    --text-muted: #5a6378;
    
    /* Border Colors */
    --border-subtle: rgba(100, 200, 255, 0.1);
    --border-normal: rgba(100, 200, 255, 0.2);
    --border-emphasis: rgba(100, 200, 255, 0.4);
}
```

### 2.2 Color Usage Guidelines

| Color | Usage | Example |
|-------|-------|---------|
| `--accent-cyan` | Primary actions, key metrics, brand elements | Anomaly Score, CTAs |
| `--status-danger` | Fraud alerts, high-risk indicators, critical errors | Fraud Detection Alert |
| `--status-warning` | Medium risk, pending review, caution states | Review Required |
| `--status-success` | Verified safe, low risk, successful operations | Transaction Cleared |
| `--text-secondary` | Supporting text, labels, metadata | Timestamps, Labels |

### 2.3 Gradient Definitions

```css
/* Primary Gradient - Quantum Effect */
--gradient-primary: linear-gradient(135deg, #00ffff 0%, #0080ff 100%);

/* Danger Gradient - Alert */
--gradient-danger: linear-gradient(135deg, #ff4757 0%, #c44569 100%);

/* Success Gradient - Safe */
--gradient-success: linear-gradient(135deg, #00d2d3 0%, #00b894 100%);

/* Background Gradient */
--gradient-background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);

/* Border Glow - Animated */
--gradient-glow: linear-gradient(45deg, #00ffff, #0080ff, #ff00ff, #ff0080);
```

---

## 3. Typography

### 3.1 Font Stack

```css
:root {
    /* Primary Font - UI Elements */
    --font-primary: 'Segoe UI', system-ui, -apple-system, sans-serif;
    
    /* Monospace - Data/Numbers */
    --font-mono: 'SF Mono', 'Fira Code', 'Consolas', monospace;
    
    /* Display - Headlines (Optional) */
    --font-display: 'Inter', 'Outfit', sans-serif;
}
```

### 3.2 Type Scale

| Level | Size | Weight | Usage |
|-------|------|--------|-------|
| H1 | 48px | 700 | Page titles, Main score display |
| H2 | 32px | 600 | Section headers |
| H3 | 24px | 600 | Card titles, Metric values |
| H4 | 18px | 600 | Subsection headers |
| Body | 14px | 400 | General content |
| Small | 12px | 400 | Labels, captions |
| Tiny | 11px | 400 | Metadata, timestamps |

### 3.3 Text Styling

```css
/* Headers */
.heading-primary {
    font-size: 48px;
    font-weight: 700;
    color: var(--accent-cyan);
    text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
}

/* Panel Headers */
.panel-header {
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--status-info);
}

/* Metric Values */
.metric-value {
    font-family: var(--font-mono);
    font-size: 24px;
    font-weight: 700;
    color: var(--text-primary);
}

/* Quantum States */
.quantum-state {
    font-family: var(--font-mono);
    color: var(--accent-cyan);
}
```

---

## 4. Component Library

### 4.1 Panel Component

```
┌─────────────────────────────────────────┐
│ ▌ PANEL HEADER          🔄 Loading     │
├─────────────────────────────────────────┤
│                                         │
│           Panel Content                 │
│                                         │
└─────────────────────────────────────────┘
```

**CSS Structure:**
```css
.panel {
    background: var(--bg-panel);
    border: 1px solid var(--border-normal);
    border-radius: 15px;
    padding: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
```

### 4.2 Metric Card

```
┌─────────────────┐
│ RECONSTRUCTION  │  ← Label (uppercase, muted)
│     0.0024      │  ← Value (large, white)
│    ↓ 12.5%      │  ← Change indicator
└─────────────────┘
```

**Variants:**
- Default (neutral)
- Positive (green indicator)
- Negative (red indicator)
- Warning (orange indicator)

### 4.3 Threat Item

```
┌─────────────────────────────────────────┐
│ ▌Card 4521               8.5/10        │
│   103.456 TBS | $2,450.00    [HIGH]    │
└─────────────────────────────────────────┘
```

**States:**
- Normal (cyan border)
- Warning (orange border)
- Critical (red border, pulsing)

### 4.4 Score Circle (Gauge)

```
       ╭───────────╮
      ╱             ╲
     │    95.2%     │   ← Animated value
     │  Anomaly     │   ← Label
      ╲   Score    ╱
       ╰───────────╯
```

**Features:**
- SVG-based circular progress
- Animated stroke-dashoffset
- Gradient stroke color
- Glow effect on value

### 4.5 Action Buttons

| Type | Style | Usage |
|------|-------|-------|
| Primary | Gradient purple/blue | Main actions |
| Success | Gradient cyan/green | Positive actions (Verify, Clear) |
| Danger | Gradient red/pink | Destructive/Alert actions |
| Secondary | Transparent with border | Secondary actions |

```css
.btn {
    padding: 12px 20px;
    border-radius: 8px;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 12px;
    letter-spacing: 1px;
    transition: all 0.3s ease;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}
```

### 4.6 Status Indicators

```
● Active    (pulsing cyan)
● Warning   (pulsing orange)
● Danger    (pulsing red)
○ Inactive  (gray, no pulse)
```

### 4.7 Modal Dialog

```
┌─────────────────────────────────────────────┐
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │ ⚡ Transaction Analysis               │  │
│  ├───────────────────────────────────────┤  │
│  │                                       │  │
│  │   Card ID: 4521    Risk: HIGH        │  │
│  │   Location: Tokyo  Amount: $2,450    │  │
│  │                                       │  │
│  │   ┌─────────────────────────────┐    │  │
│  │   │ Reconstruction Analysis:    │    │  │
│  │   │ Error exceeds threshold     │    │  │
│  │   │ by 45.2%                    │    │  │
│  │   └─────────────────────────────┘    │  │
│  │                                       │  │
│  │            [ CLOSE ]                  │  │
│  └───────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
      ↑ Backdrop (blur + dark overlay)
```

### 4.8 Toast Notifications

```
┌──────────────────────────────────────────┐
│ ⚠️  Fraud Detected on Card 4521         │
│     Transaction blocked automatically    │
└──────────────────────────────────────────┘
```

**Types:**
- Success (green left border)
- Warning (orange left border)
- Error (red left border)
- Info (blue left border)

---

## 5. Layout System

### 5.1 Grid Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│                          VIEWPORT (100vh)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐  ┌────────────────────────────────┐  ┌────────────┐  │
│  │          │  │                                │  │            │  │
│  │  LEFT    │  │           CENTER               │  │   RIGHT    │  │
│  │  PANEL   │  │           PANEL                │  │   PANEL    │  │
│  │          │  │                                │  │            │  │
│  │  300px   │  │            1fr                 │  │   350px    │  │
│  │          │  │                                │  │            │  │
│  │  Threat  │  │    3D Visualization            │  │  Deep      │  │
│  │  Matrix  │  │    Waveform                    │  │  Scan      │  │
│  │          │  │    Action Buttons              │  │  Analysis  │  │
│  │          │  │                                │  │            │  │
│  └──────────┘  └────────────────────────────────┘  └────────────┘  │
│                                                                     │
│  Gap: 20px                                    Padding: 20px         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 CSS Grid Definition

```css
.container {
    display: grid;
    grid-template-columns: 300px 1fr 350px;
    gap: 20px;
    padding: 20px;
    max-width: 1920px;
    margin: 0 auto;
    height: 100vh;
}
```

### 5.3 Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | 4px | Tight spacing, icon gaps |
| `--space-sm` | 8px | Small gaps, compact lists |
| `--space-md` | 15px | Default component spacing |
| `--space-lg` | 20px | Panel padding, section gaps |
| `--space-xl` | 30px | Large section margins |

---

## 6. User Personas

### 6.1 Primary: Fraud Analyst

```
┌─────────────────────────────────────────────────────────────┐
│  👤 PERSONA: Sarah Chen - Senior Fraud Analyst              │
├─────────────────────────────────────────────────────────────┤
│  Age: 34        Experience: 8 years                         │
│  Technical Skill: Advanced                                  │
│                                                             │
│  GOALS:                                                     │
│  • Monitor transactions in real-time                        │
│  • Quickly identify and investigate fraud patterns          │
│  • Make data-driven decisions under time pressure           │
│  • Generate reports for management                          │
│                                                             │
│  PAIN POINTS:                                               │
│  • Information overload from multiple systems               │
│  • False positives wasting investigation time               │
│  • Delayed alerts on emerging fraud patterns                │
│                                                             │
│  NEEDS FROM UI:                                             │
│  • Clear visual hierarchy for prioritization                │
│  • One-click deep-dive into suspicious transactions         │
│  • Customizable alert thresholds                            │
│  • Real-time updates without page refresh                   │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Secondary: Bank Operations Manager

```
┌─────────────────────────────────────────────────────────────┐
│  👤 PERSONA: Michael Torres - Operations Manager            │
├─────────────────────────────────────────────────────────────┤
│  Age: 45        Experience: 15 years                        │
│  Technical Skill: Intermediate                              │
│                                                             │
│  GOALS:                                                     │
│  • Monitor overall fraud detection performance              │
│  • View aggregated metrics and trends                       │
│  • Ensure SLA compliance                                    │
│  • Present insights to executive leadership                 │
│                                                             │
│  NEEDS FROM UI:                                             │
│  • Executive dashboard with KPIs                            │
│  • Exportable reports and charts                            │
│  • Historical trend analysis                                │
│  • System health monitoring                                 │
└─────────────────────────────────────────────────────────────┘
```

### 6.3 Tertiary: IT Security Officer

```
┌─────────────────────────────────────────────────────────────┐
│  👤 PERSONA: Dr. Aisha Patel - Security Officer             │
├─────────────────────────────────────────────────────────────┤
│  Age: 38        Experience: 12 years                        │
│  Technical Skill: Expert                                    │
│                                                             │
│  GOALS:                                                     │
│  • Understand quantum model behavior                        │
│  • Validate model accuracy and performance                  │
│  • Configure detection parameters                           │
│  • Audit system decisions                                   │
│                                                             │
│  NEEDS FROM UI:                                             │
│  • Model performance metrics                                │
│  • Quantum state visualization                              │
│  • Configuration panel for thresholds                       │
│  • Detailed audit logs                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. User Flows

### 7.1 Primary Flow: Fraud Investigation

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FRAUD INVESTIGATION FLOW                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     │
│   │  Alert  │────▶│  View   │────▶│Analyze  │────▶│ Action  │     │
│   │ Appears │     │ Details │     │ Pattern │     │(Block/  │     │
│   │         │     │         │     │         │     │ Clear)  │     │
│   └─────────┘     └─────────┘     └─────────┘     └─────────┘     │
│       │               │               │               │             │
│       ▼               ▼               ▼               ▼             │
│   Threat          Transaction      3D View        Confirm          │
│   Matrix          Modal Opens      Updates        Action           │
│   Highlights                                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 Secondary Flow: System Monitoring

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SYSTEM MONITORING FLOW                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     │
│   │ Login   │────▶│Overview │────▶│ Check   │────▶│ Adjust  │     │
│   │ to      │     │Dashboard│     │ Metrics │     │ Config  │     │
│   │ System  │     │         │     │         │     │         │     │
│   └─────────┘     └─────────┘     └─────────┘     └─────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.3 Tertiary Flow: What-If Simulation

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WHAT-IF SIMULATION FLOW                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     │
│   │ Select  │────▶│Configure│────▶│  Run    │────▶│ Review  │     │
│   │Scenario │     │ Params  │     │Simulate │     │ Results │     │
│   │         │     │         │     │         │     │         │     │
│   └─────────┘     └─────────┘     └─────────┘     └─────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 8. Page Structure

### 8.1 Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│                         HEADER (Optional)                           │
│  ⚛️ QuantumEye v2.0                    👤 User    🔔 Alerts    ⚙️  │
├──────────────┬────────────────────────────────────┬─────────────────┤
│              │                                    │                 │
│  LEFT PANEL  │         CENTER PANEL               │   RIGHT PANEL   │
│              │                                    │                 │
│ ┌──────────┐ │  ┌──────────────────────────────┐ │ ┌─────────────┐ │
│ │ Threat   │ │  │        Status Bar            │ │ │   Anomaly   │ │
│ │ Matrix   │ │  │  ● Active     14:32:05       │ │ │   Score     │ │
│ │          │ │  └──────────────────────────────┘ │ │   Gauge     │ │
│ │ Card 4521│ │                                   │ │             │ │
│ │ Card 3892│ │  ┌──────────────────────────────┐ │ └─────────────┘ │
│ │ Card 7234│ │  │                              │ │                 │
│ │ Card 1567│ │  │    3D Reconstruction         │ │ ┌─────────────┐ │
│ │ Card 8901│ │  │    Visualization             │ │ │   Metrics   │ │
│ │ Card 2345│ │  │                              │ │ │   Grid      │ │
│ │ Card 6789│ │  │                              │ │ │             │ │
│ │ Card 0123│ │  └──────────────────────────────┘ │ └─────────────┘ │
│ │ Card 4567│ │                                   │                 │
│ │ Card 8901│ │  ┌──────────────────────────────┐ │ ┌─────────────┐ │
│ │          │ │  │    Waveform Animation        │ │ │  Predictive │ │
│ └──────────┘ │  └──────────────────────────────┘ │ │  Factors    │ │
│              │                                   │ │             │ │
│              │  ┌────────┬────────┬────────────┐ │ └─────────────┘ │
│              │  │Simulate│ Verify │  Toggle    │ │                 │
│              │  │ Attack │& Clear │ Rotation   │ │                 │
│              │  └────────┴────────┴────────────┘ │                 │
│              │                                   │                 │
└──────────────┴───────────────────────────────────┴─────────────────┘
```

### 8.2 Component Hierarchy

```
Dashboard
├── Header (optional)
│   ├── Logo
│   ├── Navigation
│   └── User Menu
│
├── Left Panel: Threat Matrix
│   ├── Panel Header
│   ├── Loading Indicator
│   └── Threat Items List
│       └── Threat Item [n]
│           ├── Card ID
│           ├── Threat Details
│           └── Score Badge
│
├── Center Panel: Visualization
│   ├── Status Bar
│   │   ├── Status Indicator
│   │   └── Timestamp
│   ├── 3D Reconstruction Container
│   │   ├── Three.js Canvas
│   │   └── Graph Legend
│   ├── Waveform Container
│   │   └── Waveform Canvas
│   └── Button Group
│       ├── Simulate Attack Button
│       ├── Verify & Clear Button
│       └── Toggle Rotation Button
│
├── Right Panel: Analysis
│   ├── Anomaly Score Gauge
│   │   ├── SVG Circle
│   │   ├── Score Value
│   │   └── Score Label
│   ├── Metrics Grid
│   │   ├── Reconstruction Error Card
│   │   ├── Threshold Card
│   │   ├── Quantum State Card
│   │   └── Confidence Card
│   └── Predictive Factors List
│       ├── Behavioral Deviation
│       ├── Geo-Temporal Irregularity
│       └── Device Fingerprint Mismatch
│
└── Modal Dialog
    ├── Modal Backdrop
    └── Modal Content
        ├── Title
        ├── Metrics Grid
        ├── Analysis Text
        └── Close Button
```

---

## 9. Interaction Patterns

### 9.1 Hover States

| Element | Hover Effect |
|---------|--------------|
| Threat Item | Slide right 5px, lighten background |
| Metric Card | Lift up 2px, lighten background |
| Button | Lift up 2px, add shadow glow |
| Panel | Subtle border glow animation |

### 9.2 Click/Tap Interactions

| Element | Action |
|---------|--------|
| Threat Item | Open transaction detail modal |
| Simulate Attack | Trigger visual attack simulation |
| Verify & Clear | Clear current transaction, update metrics |
| Toggle Rotation | Enable/disable 3D rotation |
| Modal Backdrop | Close modal |

### 9.3 Real-Time Updates

| Data | Update Interval | Animation |
|------|-----------------|-----------|
| Threat Matrix | 1 second | Fade in new items |
| Metrics | 3 seconds | Number count animation |
| Timestamp | 1 second | Direct update |
| 3D Visualization | 60fps | Continuous rotation |
| Waveform | 60fps | Continuous wave |

### 9.4 Loading States

```
┌──────────────────────────────────────┐
│ ▌ PANEL HEADER        ⟳ Loading     │   ← Spinning indicator
├──────────────────────────────────────┤
│                                      │
│     ████████░░░░░░░░░░  40%         │   ← Progress bar (if applicable)
│                                      │
│     Loading transactions...          │   ← Status text
│                                      │
└──────────────────────────────────────┘
```

### 9.5 Error States

```
┌──────────────────────────────────────┐
│ ▌ PANEL HEADER                       │
├──────────────────────────────────────┤
│                                      │
│     ⚠️ Connection Error             │   ← Error icon
│                                      │
│     Unable to fetch data.           │
│     [ Retry ]                        │   ← Action button
│                                      │
└──────────────────────────────────────┘
```

---

## 10. Accessibility Guidelines

### 10.1 Color Contrast

| Text Type | Minimum Ratio | Our Ratio |
|-----------|---------------|-----------|
| Body text | 4.5:1 | ✅ 7.2:1 |
| Large text | 3:1 | ✅ 5.8:1 |
| UI components | 3:1 | ✅ 4.5:1 |

### 10.2 ARIA Labels

```html
<!-- Example ARIA implementation -->
<button class="btn danger" 
        aria-label="Simulate cyber attack scenario"
        role="button">
    Simulate Attack
</button>

<div role="alert" 
     aria-live="polite" 
     aria-label="Current anomaly score">
    95.2%
</div>

<div class="threat-item" 
     role="listitem"
     tabindex="0"
     aria-label="Transaction Card 4521, risk score 8.5 out of 10">
    <!-- content -->
</div>
```

### 10.3 Keyboard Navigation

| Key | Action |
|-----|--------|
| Tab | Navigate between interactive elements |
| Enter/Space | Activate focused button/link |
| Escape | Close modal |
| Arrow Keys | Navigate within threat list |

### 10.4 Screen Reader Support

- All images have descriptive `alt` text
- Dynamic content updates use `aria-live` regions
- Form controls have associated labels
- Heading hierarchy is logical (h1 → h2 → h3)

---

## 11. Responsive Design

### 11.1 Breakpoints

```css
/* Desktop Large */
@media (min-width: 1440px) {
    .container {
        grid-template-columns: 350px 1fr 400px;
    }
}

/* Desktop */
@media (min-width: 1024px) and (max-width: 1439px) {
    .container {
        grid-template-columns: 300px 1fr 350px;
    }
}

/* Tablet */
@media (min-width: 768px) and (max-width: 1023px) {
    .container {
        grid-template-columns: 1fr 1fr;
        grid-template-rows: auto auto auto;
        height: auto;
    }
    .panel:nth-child(2) {
        grid-column: span 2;
    }
}

/* Mobile */
@media (max-width: 767px) {
    .container {
        grid-template-columns: 1fr;
        height: auto;
        padding: 10px;
    }
    .metrics-grid {
        grid-template-columns: 1fr;
    }
    .button-group {
        flex-direction: column;
    }
}
```

### 11.2 Responsive Layout Visualization

**Desktop (1920px)**
```
┌──────┬──────────────────┬──────┐
│ Left │      Center      │Right │
│ 300px│       1fr        │350px │
└──────┴──────────────────┴──────┘
```

**Tablet (768px - 1023px)**
```
┌──────────────────────────────┐
│           Center             │
├──────────────┬───────────────┤
│    Left      │     Right     │
│    1fr       │     1fr       │
└──────────────┴───────────────┘
```

**Mobile (< 768px)**
```
┌─────────────────┐
│     Left        │
├─────────────────┤
│     Center      │
├─────────────────┤
│     Right       │
└─────────────────┘
```

---

## 12. Animation & Motion

### 12.1 Animation Principles

| Principle | Application |
|-----------|-------------|
| **Purposeful** | Every animation serves a functional purpose |
| **Quick** | Transitions under 300ms for UI, 1s for emphasis |
| **Smooth** | Use easing functions (ease-out, ease-in-out) |
| **Subtle** | Avoid distracting from data |

### 12.2 Timing Functions

```css
/* Standard UI transitions */
--ease-standard: cubic-bezier(0.4, 0.0, 0.2, 1);  /* 300ms */

/* Entry animations */
--ease-decelerate: cubic-bezier(0.0, 0.0, 0.2, 1);  /* 250ms */

/* Exit animations */
--ease-accelerate: cubic-bezier(0.4, 0.0, 1, 1);  /* 200ms */

/* Emphasis animations */
--ease-emphasis: cubic-bezier(0.4, 0.0, 0.6, 1);  /* 500ms */
```

### 12.3 Key Animations

**Border Glow**
```css
@keyframes borderGlow {
    0%, 100% { opacity: 0; }
    50% { opacity: 0.3; }
}
/* Duration: 3s, Timing: ease-in-out */
```

**Pulse (Status Indicators)**
```css
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
/* Duration: 2s, Timing: ease */
```

**Spin (Loading)**
```css
@keyframes spin {
    to { transform: rotate(360deg); }
}
/* Duration: 1s, Timing: linear */
```

**Score Circle Fill**
```css
.score-circle circle {
    transition: stroke-dashoffset 1s ease;
}
```

### 12.4 3D Animation (Three.js)

```javascript
// Continuous rotation
function animate3D() {
    requestAnimationFrame(animate3D);
    
    if (rotationEnabled) {
        originalLine.rotation.y += 0.005;      // ~0.3°/frame
        reconstructedLine.rotation.y += 0.005;
        anomalyPoints.rotation.y += 0.005;
    }
    
    renderer.render(scene, camera);
}
```

---

## 📎 Appendix: Quick Reference

### Color Cheat Sheet

| Purpose | Color Code | CSS Variable |
|---------|------------|--------------|
| Safe/Normal | #00d2d3 | `--status-success` |
| Warning/Medium | #ffa502 | `--status-warning` |
| Danger/High | #ff4757 | `--status-danger` |
| Quantum Accent | #00ffff | `--accent-cyan` |
| Background | #0a0e27 | `--bg-primary` |

### Component Quick Reference

| Component | Class | Used For |
|-----------|-------|----------|
| Panel | `.panel` | Main containers |
| Threat Item | `.threat-item` | Transaction rows |
| Metric Card | `.metric-card` | KPI display |
| Button | `.btn` | Actions |
| Score Gauge | `.score-circle` | Main metric |
| Modal | `.modal` | Dialogs |

---

## 📄 Document Information

| Field | Value |
|-------|-------|
| **Project** | QuantumEye v2.0 |
| **Document** | UI/UX Framework |
| **Version** | 1.0 |
| **Created** | February 2026 |
| **Author** | QuantumEye Development Team |

---

*This framework serves as the single source of truth for all UI/UX decisions in the QuantumEye project.*
