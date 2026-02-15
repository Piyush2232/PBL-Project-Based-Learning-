# PBL (Project Based Learning)

**Author:** Piyush Prakash Sharma  
**Status:** Ongoing  

## Project Overview
This project is a **Finance Tracker** application developed as part of a Project Based Learning (PBL). It automates the process of analyzing personal finance data by processing CSV transaction logs and generating comprehensive Excel reports.

## Features
- **Automated Categorization**: Automatically categorizes transactions into groups like *Food, Travel, Shopping, Bills, Subscriptions,* and *Groceries* based on keyword matching.
- **Data Cleaning**: Handles various currency formats, removes special characters, and normalizes transaction amounts.
- **Visual Reporting**: Generates an Excel workbook containing:
    - **Transactions Sheet**: Cleaned and categorized raw data.
    - **Summary Sheet**: Aggregated spending by category.
    - **Visualization**: A built-in Pie Chart showing spending distribution.

## Project Structure
- `finance_tracker.py`: The main Python script containing the logic for data processing and report generation.
- `PBL_Report.docx` / `PBL.pptx`: Documentation and presentation materials for the project.

## Requirements
- Python 3.x
- `pandas`
- `openpyxl`

## Usage
Run the script with your transaction CSV file as an argument:

```sh
python finance_tracker.py <path_to_csv>
```

The script will generate a `finance_report.xlsx` file in the current directory.
