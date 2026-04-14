# 🪶 FinTracker

**Author:** Piyush Prakash Sharma  
**Status:** Active Development
---

## Overview

FinTracker is a personal finance and budgeting application designed to actively disincentivize overspending .Unlike commercial products (Gpay ,PhonePe etc)that scrape data and use toxic positive reinforcement like cashbacks and cupons etc. to encourage spending, FinTracker focuses solely on helping you set goals and build financial responsibility. It is sort of a mix of a finance app and duolingo .The same way Duolingo doesn't reward you with money; it rewards you with psychological momentum (the Streak), and more importantly, it uses the fear of losing that momentum (passive-aggressive notifications) to force you to behave, it also relies on feedback loops and daily/monthly saving streaks to hold you accountable.

This prototype version processes CSV transaction logs using **Machine Learning (Naive Bayes NLP classifier)** for **smart expense categorization** and renders a real-time **isometric dashboard**. It also generates Excel reports with charts and budget analysis.

The core idea of the application is :
- Whenever you spend your money through online methods the app reads your transaction through messages and then      notifies you how close you are to reaching your monthly/daily budget limit sort of like breaking the "Savings streak"
- If by the end of the day you exceeded your daily budget limit then the app can reset your streak or give you an option to keep your streak by spending less the next day. 
- It will also provide user with downloadable detailed reports of their transactions with charts and budget analysis

---

## ✨ Features

### ML Engine (`finance_tracker.py` + `train_model.py`)
- **Categorization using Naive Bayes Classifier** — TF-IDF vectorizer + Multinomial Naive Bayes classifier trained on labeled transaction data
- **Fallback** — Keyword-matching engine activates automatically if ML model files are missing
- **Data Cleaning** — Handles ₹ symbols, commas, parenthetical negatives, and mixed formats
- **Excel Reports** — Color-coded transactions, summary sheets, and embedded pie charts via `openpyxl`

### Data Generation (`generate_large_csv.py`)
- **Synthetic Datasets** — Uses `Faker` to generate realistic test transaction CSVs with 500+ entries


### Backend (`app.py`)
- **Flask API** — Serves the dashboard and handles CSV uploads via `/api/upload`
- **Real-time Processing** — Uploads are categorized, analyzed, and returned as JSON in a single request
- **Budget Analysis** — Compares spending against user-defined budget limits
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
