from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='./frontend/build', static_url_path='/')
CORS(app)  # Enable CORS for all routes
DATA_FILE = 'data/spending.csv'

os.makedirs('data', exist_ok=True)
if not os.path.isfile(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Item", "Amount"])
    df.to_csv(DATA_FILE, index=False)

# Serve React App
@app.route('/')
def index():
    return app.send_static_file('index.html')

# API Routes
@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    df = pd.read_csv(DATA_FILE)
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.json
    date = data['date']
    category = data['category']
    item = data['item']
    amount = float(data['amount'])

    new_entry = pd.DataFrame([[date, category, item, amount]], columns=["Date", "Category", "Item", "Amount"])
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    return jsonify({"success": True})

# Legacy routes (can be removed later)
@app.route('/report')
def report():
    df = pd.read_csv(DATA_FILE)
    return render_template('report.html', data=df.to_dict(orient='records'))

@app.route('/add', methods=['POST'])
def add_expense_form():
    date = request.form['date']
    category = request.form['category']
    item = request.form['item']
    amount = float(request.form['amount'])

    new_entry = pd.DataFrame([[date, category, item, amount]], columns=["Date", "Category", "Item", "Amount"])
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    return redirect('/report')

if __name__ == '__main__':
    app.run(debug=True)
