import pandas as pd
import re
import os
from openpyxl import Workbook
from openpyxl.chart import PieChart, Reference
from openpyxl.utils.dataframe import dataframe_to_rows

# CATEGORY MAPPING
CATEGORY_KEYWORDS = {
    "Food": ["swiggy", "zomato", "mcdonald", "kfc", "restaurant", "food", "cafe"],
    "Travel": ["uber", "ola", "train", "flight", "bus", "petrol", "auto"],
    "Shopping": ["amazon", "flipkart", "myntra", "ajio"],
    "Bills": ["electricity", "internet", "wifi", "broadband", "bill"],
    "Subscriptions": ["netflix", "spotify", "hotstar", "prime"],
    "Groceries": ["grocery", "dmart", "big bazaar", "supermarket"],
    "Others": []
}

# CLEAN CATEGORY
def categorize(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return category
    return "Others"

# CLEAN AMOUNT (handles ₹, commas, parentheses, etc.)
def clean_amount_column(df):
    df["Amount"] = (
        df["Amount"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.replace("(", "-", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace(" ", "", regex=False)
    )
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0)
    return df

# MAIN FUNCTION
def convert_and_chart(csv_file, xlsx_file="finance_report.xlsx"):
    # Load CSV
    df = pd.read_csv(csv_file)

    # Normalize columns
    df.columns = [c.strip() for c in df.columns]

    # Required columns
    if "Description" not in df.columns or "Amount" not in df.columns:
        raise ValueError("CSV must include 'Description' and 'Amount' columns.")

    # Clean Amount field
    df = clean_amount_column(df)

    # Categorize
    df["Description"] = df["Description"].astype(str)
    df["Category"] = df["Description"].apply(categorize)

    # Expenses only
    df_exp = df[df["Amount"] < 0].copy()
    df_exp["AbsAmount"] = df_exp["Amount"].abs()

    summary = df_exp.groupby("Category")["AbsAmount"].sum().reset_index()

    # BUILD THE EXCEL FILE
    wb = Workbook()

    # Sheet 1 → Raw Data
    ws1 = wb.active
    ws1.title = "Transactions"

    for r in dataframe_to_rows(df, index=False, header=True):
        ws1.append(r)

    # Sheet 2 → Summary
    ws2 = wb.create_sheet("Summary")

    for r in dataframe_to_rows(summary, index=False, header=True):
        ws2.append(r)

    # PIE CHART CREATION

    if summary.empty:
        print("No expenses found. Excel file created WITHOUT pie chart.")
        wb.save(xlsx_file)
        os.startfile(xlsx_file)
        return

    if len(summary) == 1:
        print("Only one category found. Pie chart may not display well.")

    pie = PieChart()
    pie.title = "Spending by Category"

    start_row = 2
    end_row = len(summary) + 1

    labels = Reference(ws2, min_col=1, min_row=start_row, max_row=end_row)
    data   = Reference(ws2, min_col=2, min_row=1, max_row=end_row)

    pie.add_data(data, titles_from_data=True)
    pie.set_categories(labels)

    ws2.add_chart(pie, "D2")

    # Save Excel
    base = "finance_report"
    counter = 1
    final_name = f"{base}.xlsx"

    while os.path.exists(final_name):
        counter += 1
        final_name = f"{base}_{counter}.xlsx"

    wb.save(final_name)
    print("Saved as:", final_name)
    os.startfile(final_name)


    print("\nExcel file created successfully:", xlsx_file)
    print("Sheets generated: Transactions, Summary + Pie Chart")

    # Auto-open (Windows only)
    try:
        os.startfile(xlsx_file)
    except:
        pass

# RUNNER
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python csv_to_excel_pie.py yourfile.csv")
        exit()

    csv_path = sys.argv[1]
    convert_and_chart(csv_path)

