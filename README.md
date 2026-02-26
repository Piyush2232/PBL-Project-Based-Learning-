# PBL (Project Based Learning) - Finance Tracker

**Author:** Piyush Prakash Sharma  
**Status:** Ongoing  

## Project Overview
This project is an automated **Finance Tracker** application. It processes CSV transaction logs and generates comprehensive, styled Excel reports. The project has recently been refactored to use an Object-Oriented design and now incorporates **Machine Learning (Naive Bayes classifier)** for smart transaction categorization.

## Features
- **AI-Powered Categorization**: Uses an NLP Machine Learning model (`scikit-learn`) to intelligently categorize transactions based on description.
- **Robust Fallback Logic**: Automatically falls back to keyword-matching if the ML model is not available.
- **Data Generation**: Includes a script (`generate_large_csv.py`) that uses `Faker` to generate synthetic transaction data for testing.
- **Smart Data Cleaning**: Handles various currency formats, extracts negative/positive balances correctly, and tracks Income vs. Expenses.
- **Visual Excel Reporting**: Generates a beautiful Excel workbook using `openpyxl` with:
    - **Transactions Sheet**: Cleaned raw data, color-coded for income (green) and expenses (red).
    - **Summary Sheet**: Financial overview and aggregated spending.
    - **Visualization**: A built-in Pie Chart showing spending distribution based on categories.

## Project Structure
- `finance_tracker.py`: The main Object-Oriented Python script.
- `train_model.py`: Script to train the Machine Learning categorization model.
- `generate_large_csv.py`: Generates fake test transaction datasets.
- `PBL_Report.docx` / `PBL.pptx`: Documentation and presentation materials.

## Requirements
```sh
pip install pandas openpyxl scikit-learn joblib faker
```

## Setup & Usage

### 1. Generate Test Data (Optional)
If you don't have your own CSV dataset, generate one:
```sh
python generate_large_csv.py
```
This creates a `large_transactions.csv` file with 500 unique synthetic transactions.

### 2. Train the AI Model
Train the text-classification model so the finance tracker can smartly categorize expenses:
```sh
python train_model.py
```
This generates `expense_model.pkl` and `expense_vectorizer.pkl`.

### 3. Run the Finance Tracker
Process your CSV file and generate the styled Excel report:
```sh
python finance_tracker.py <path_to_csv>
```
*Example:* `python finance_tracker.py large_transactions.csv`

**Optional Flags:**
- `-o` or `--output`: Specify a custom prefix for the generated Excel file.
- `--no-ml`: Force disable the Machine Learning categorizer and use the hardcoded keyword fallback method.
