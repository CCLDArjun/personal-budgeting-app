from flask import Flask, render_template, request, redirect
import pandas as pd
import os

app = Flask(__name__)
DATA_FILE = 'data/spending.csv'

os.makedirs('data', exist_ok=True)
if not os.path.isfile(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Item", "Amount"])
    df.to_csv(DATA_FILE, index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    df = pd.read_csv(DATA_FILE)
    return render_template('report.html', data=df.to_dict(orient='records'))

@app.route('/add', methods=['POST'])
def add_expense():
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
