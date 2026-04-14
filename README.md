# 🪶 FinTracker — AI-Powered Finance Dashboard

**Author:** Piyush Prakash Sharma  
**Status:** Active Development  
**Stack:** Python · Flask · React · scikit-learn

---

## Overview

FinTracker is a full-stack personal finance application that processes CSV transaction logs using **Machine Learning (Naive Bayes NLP classifier)** for smart expense categorization and renders a real-time **isometric dashboard** with emotional spending feedback. It also generates styled Excel reports with charts and budget analysis.

The core idea: **make your spending habits feel visceral.** The app doesn't just show you numbers — it makes you *feel* overspending through red-pulsing borders, shaking alarm icons, and urgent messaging. Conversely, staying under budget rewards you with calming cyan glows and celebratory badges.

---

## ✨ Features


### Backend (`app.py`)
- **Flask API** — Serves the dashboard and handles CSV uploads via `/api/upload`
- **Real-time Processing** — Uploads are categorized, analyzed, and returned as JSON in a single request
- **Budget Analysis** — Compares spending against user-defined budget limits

### ML Engine (`finance_tracker.py` + `train_model.py`)
- **AI-Powered Categorization** — TF-IDF vectorizer + Multinomial Naive Bayes classifier trained on labeled transaction data
- **Robust Fallback** — Keyword-matching engine activates automatically if ML model files are missing
- **Smart Data Cleaning** — Handles ₹ symbols, commas, parenthetical negatives, and mixed formats
- **Styled Excel Reports** — Color-coded transactions, summary sheets, and embedded pie charts via `openpyxl`

### Data Generation (`generate_large_csv.py`)
- **Synthetic Datasets** — Uses `Faker` to generate realistic test transaction CSVs with 500+ entries

---

## 📁 Project Structure

```
Project/
├── app.py                    # Flask server — serves dashboard & API
├── finance_tracker.py        # Core OOP module — categorizer + Excel generator
├── train_model.py            # ML training script (Naive Bayes + TF-IDF)
├── generate_large_csv.py     # Synthetic test data generator (Faker)
├── expense_model.pkl         # Trained ML model (auto-generated)
├── expense_vectorizer.pkl    # TF-IDF vectorizer (auto-generated)
├── training_data*.csv        # Labeled training datasets
├── test_transactions.csv     # Sample transaction CSV for testing
├── site/
│   ├── index.html            # React SPA — isometric dashboard with emotional feedback
│   ├── style.css             # Legacy styles (original dashboard)
│   └── script.js             # Legacy scripts (original dashboard)
└── Reports&ppts/             # Documentation & presentation materials
```

---

## ⚙️ Requirements

```sh
pip install flask pandas openpyxl scikit-learn joblib faker
```

**Python 3.8+** required.

---

## 🚀 Setup & Usage

### 1. Train the AI Model
```sh
python train_model.py
```
Trains on all `training_data*.csv` files and saves `expense_model.pkl` + `expense_vectorizer.pkl`.  
Outputs accuracy score and a detailed classification report.

### 2. Generate Test Data *(optional)*
```sh
python generate_large_csv.py
```
Creates `test_transactions.csv` with 500 synthetic transactions.

### 3. Launch the Dashboard
```sh
python app.py
```
Opens at **http://localhost:5000**. The flow:
1. Set your monthly budget limit
2. Upload a transaction CSV
3. The dashboard renders with rings, emotional borders, and real-time analytics
4. Click the center circle to bloom category rings
5. Download the Excel report from the footer

### 4. CLI Mode *(no server)*
Process a CSV directly and generate an Excel report:
```sh
python finance_tracker.py <path_to_csv>
```
**Flags:**
| Flag | Description |
|------|-------------|
| `-o`, `--output` | Custom prefix for the Excel output file |
| `--no-ml` | Force keyword-only categorization (skip ML) |

---

## 🎨 Design Philosophy

The dashboard uses a **pitch-black isometric aesthetic** with:
- **JetBrains Mono** for numerical data, **Syne** for headings
- Glassmorphism panels with `backdrop-filter: blur`
- Isometric grid background with a traveling scanline
- SVG ring animations with `strokeDasharray` transitions
- CSS keyframe animations for border pulses, corner glows, and icon bounces

The emotional feedback is intentionally aggressive — the goal is to create a **visceral financial awareness** that generic pie charts can't achieve.

---

## 📊 API Reference

### `POST /api/upload`
Upload a transaction CSV for processing.

**Form Data:**
| Field | Type | Description |
|-------|------|-------------|
| `file` | File | CSV with `Description` and `Amount` columns |
| `budget_limit` | Number | Monthly budget threshold (default: 50000) |

**Response:**
```json
{
  "success": true,
  "total_income": 50000.0,
  "total_expense": 9128.0,
  "summary": { "Food": 1250, "Shopping": 3500, ... },
  "recent": [ ... ],
  "excel_url": "/api/download/finance_report.xlsx",
  "status_message": "Great job! You stayed under budget...",
  "budget_pct": 18.3
}
```

### `GET /api/download/<filename>`
Download the generated Excel report.

---

## 📄 License

Academic project — PBL (Project Based Learning) 2026.
