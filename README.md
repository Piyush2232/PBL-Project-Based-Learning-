# Finance Tracker (PBL Project)

**Author:** Piyush Prakash Sharma  
**Status:** Ongoing  

## Project Goal
The main goal of this project is to build a smart, automated tool that takes messy bank transaction data (like a raw CSV export) and turns it into a clear, visual financial report. Instead of manually grouping every single coffee shop run or taxi ride into a spreadsheet to see where my money goes, I wanted to write a Python script that figures it out for me and builds a clean Excel dashboard automatically.

## How it Works
1. **Data Cleaning:** The script first ingests a raw CSV. It cleans up the messy formatting (stripping out currency symbols, handling parentheses for negative balances, and turning everything into usable numbers).
2. **Smart Categorization (AI!):** Instead of just checking if a description contains the word "Uber", it uses a simple Machine Learning model (Naive Bayes) to read the transaction text and predict what bucket it belongs in (Food, Travel, Subscriptions, Bills, Groceries, Shopping, etc.).
3. **Excel Generation:** Finally, it uses `openpyxl` to build a beautifully formatted `.xlsx` file from scratch. It creates a bolded, color-coded list of transactions (green for income, red for expenses), builds a summary table of net balances, and drops in a pie chart so you can instantly see where your most expensive habits are.

## What's included in the Repo
- `finance_tracker.py`: The main script that does all the heavy lifting and building the Excel sheet.
- `train_model.py`: A script to train the AI model on historical expense data.
- `generate_large_csv.py`: I use this to quickly generate fake, randomized transaction data for testing (using the `Faker` library).
- `PBL_Report.docx` & `PBL.pptx`: The actual write-up and slides for my project submission.

## Setup
You'll need a few packages to run everything. Just install them via pip:
```sh
pip install pandas openpyxl scikit-learn joblib faker
```

## How to run it

### 1. Training the model (Optional but recommended)
Before running the main tracker, you should probably train the classification model so it knows how to categorize things. Just run:
```sh
python train_model.py
```
*(This spits out `expense_model.pkl` and `expense_vectorizer.pkl` which the main script will look for).*

### 2. Testing with fake data (Optional)
If you just want to see how the script works but don't want to use your real bank statements, you can generate 500 fake records:
```sh
python generate_large_csv.py
```

### 3. Running the tracker
To actually parse a CSV and get your styled Excel report, just pass your CSV file to the main script:
```sh
python finance_tracker.py your_csv_file.csv
```
*(For example: `python finance_tracker.py large_transactions.csv`)*

**Extra command-line tricks:**
- Want to name the output file something specific? Use `-o file_name`.
- Break the ML model? Use `--no-ml` to force the script to fall back to the basic keyword-matching method.
