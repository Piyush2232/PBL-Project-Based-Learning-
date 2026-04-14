import os
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from finance_tracker import TransactionCategorizer, FinanceReportGenerator
import logging

app = Flask(__name__, static_folder='site')
categorizer = TransactionCategorizer(force_fallback=False)

@app.route('/')
def index():
    return send_from_directory('site', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('site', path)

@app.route('/api/download/<filename>')
def download_report(filename):
    return send_from_directory('.', filename, as_attachment=True)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    budget_limit_str = request.form.get('budget_limit', '50000')
    try:
        budget_limit = float(budget_limit_str)
    except ValueError:
        budget_limit = 50000.0

    if file:
        filepath = 'temp_upload.csv'
        file.save(filepath)
        
        try:
            # First logic: Get Excel output
            generator = FinanceReportGenerator(categorizer)
            generator.process_csv(filepath)
            excel_filename = generator.export_excel("finance_report", budget_limit=budget_limit, auto_open=False)
        
            # Parse data for the dashboard stats
            df = pd.read_csv(filepath, on_bad_lines='skip')
            
            # Use same cleaning logic as tracker
            if "Amount" in df.columns:
                df["Amount"] = df["Amount"].astype(str).str.replace(",", "", regex=False).str.replace("₹", "", regex=False).str.replace(" ", "", regex=False)
                mask_parentheses = df["Amount"].str.startswith("(") & df["Amount"].str.endswith(")")
                df.loc[mask_parentheses, "Amount"] = "-" + df.loc[mask_parentheses, "Amount"].str[1:-1]
                df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0)
            else:
                return jsonify({'error': 'CSV must contain an Amount column'}), 400
            
            if "Description" in df.columns:
                df["Category"] = df["Description"].astype(str).apply(categorizer.categorize)
            else:
                return jsonify({'error': 'CSV must contain a Description column'}), 400
            
            # Segregate Analytics
            df_exp = df[df["Amount"] < 0].copy()
            df_exp["AbsAmount"] = df_exp["Amount"].abs()
            df_inc = df[df["Amount"] > 0].copy()
            
            # Format numbers to regular floats
            summary = df_exp.groupby("Category")["AbsAmount"].sum().to_dict()
            summary = {k: float(v) for k, v in summary.items()}
            
            total_expense = float(df_exp["AbsAmount"].sum())
            total_income = float(df_inc["Amount"].sum())
            
            # Alert logic
            status_message = ""
            if total_expense > budget_limit:
                status_message = f"Warning: You exceeded your budget by ₹{total_expense - budget_limit}! 😓"
            else:
                status_message = f"Great job! You stayed under your budget by ₹{budget_limit - total_expense}! 🎉"
            
            # Format recent records safely
            full_df = df.copy()
            full_df['Amount'] = full_df['Amount'].astype(float)
            recent = full_df[['Description', 'Amount', 'Category']].to_dict('records')
            
            return jsonify({
                'success': True,
                'total_income': total_income,
                'total_expense': total_expense,
                'summary': summary,
                'recent': recent,
                'excel_url': f'/api/download/{excel_filename}',
                'status_message': status_message,
                'budget_pct': round(total_expense / budget_limit * 100, 1) if budget_limit > 0 else 0
            })
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
