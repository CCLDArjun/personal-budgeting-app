import dash
from dash import Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import os
import pandas as pd
from google.cloud import storage
import io
from flask import request
from collections import defaultdict
import json

USE_GCS = os.environ.get('USE_GCS', '0') == '1'  # Default: use local file

DEFAULT_CATEGORIES = [
    "Groceries",
    "Entertainment",
    "Transport",
    "Utilities",
    "Dining",
    "Shopping",
    "Health",
    "Other"
]

if USE_GCS:
    BUCKET_NAME = 'cs122-group5.appspot.com'
    BLOB_NAME = 'spending.csv'
    def load_data():
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(BLOB_NAME)
        data = blob.download_as_bytes()
        df = pd.read_csv(io.BytesIO(data))
        df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
        if 'Username' not in df.columns:
            df['Username'] = None
        return df
    def save_data(df):
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(BLOB_NAME)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')
else:
    DATA_FILE = 'data/spending.csv'
    def load_data():
        df = pd.read_csv(DATA_FILE)
        df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
        if 'Username' not in df.columns:
            df['Username'] = None
        return df
    def save_data(df):
        df.to_csv(DATA_FILE, index=False)

GOALS_FILE = 'data/goals.json'
def load_goals():
    goals = defaultdict(lambda: {'monthly': 0, 'yearly': 0})
    if os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, 'r') as f:
            goals_dict = json.load(f)
            for username, goal in goals_dict.items():
                goals[username]['monthly'] = goal.get('monthly', 0)
                goals[username]['yearly'] = goal.get('yearly', 0)
    return goals

def store_goals(goals):
    with open(GOALS_FILE, 'w') as f:
        json.dump(goals, f)


def get_category_options(df=None):
    return [{'label': c, 'value': c} for c in sorted(DEFAULT_CATEGORIES)]

def get_table_columns():
    return [
        {'name': 'Date', 'id': 'Date'},
        {'name': 'Category', 'id': 'Category'},
        {'name': 'Item', 'id': 'Item'},
        {'name': 'Amount', 'id': 'Amount', 'type': 'numeric', 'format': {'specifier': '$.2f'}}
    ]

def create_graphs(df):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df = df[df['Date'].notna()]
    df = df.sort_values('Date')
    category_totals = df.groupby('Category')['Amount'].sum().reset_index()
    pie_fig = px.pie(category_totals, values='Amount', names='Category', title='Spending by Category')
    line_fig = px.line(df, x='Date', y='Amount', title='Spending Over Time')
    return pie_fig, line_fig


def color(progress):
    if progress < 50:
        return 'success'
    elif progress < 80:
        return 'warning'
    else:
        return 'danger'

def create_goal_graphs(df, username):
    goals = load_goals()
    monthly_spent = df[df['Date'] >= pd.to_datetime('now') - pd.DateOffset(months=1)]['Amount'].sum()
    yearly_spent = df[df['Date'] >= pd.to_datetime('now') - pd.DateOffset(years=1)]['Amount'].sum()

    monthly = (monthly_spent / goals[username]['monthly']) * 100 if goals[username]['monthly'] else 0
    yearly = (yearly_spent / goals[username]['yearly']) * 100 if goals[username]['yearly'] else 0

    monthly = round(monthly, 2)
    yearly = round(yearly, 2)

    monthly_color = color(monthly)
    yearly_color = color(yearly)

    return monthly, f"${goals[username]['monthly']} - {monthly}%", monthly_color, yearly, f"${goals[username]['yearly']} - {yearly}%", yearly_color

def register_expenses_callbacks(app):
    @app.callback(
        [Output('expenses-table', 'data'),
         Output('pie-chart', 'figure'),
         Output('line-chart', 'figure')],
        Input('add-expense-button', 'n_clicks'),
        State('expense-date', 'value'),
        State('expense-category', 'value'),
        State('expense-item', 'value'),
        State('expense-amount', 'value'),
        prevent_initial_call=True
    )
    def update_all(n_clicks, date, category, item, amount):
        if n_clicks is None or not all([date, category, item, amount]):
            empty_fig = go.Figure()
            return dash.no_update, empty_fig, empty_fig
        
        username = request.cookies.get('username')
        df = load_data()
        new_entry = pd.DataFrame([[date, category, item, float(amount), username]], columns=["Date", "Category", "Item", "Amount", "Username"])
        df = pd.concat([df, new_entry], ignore_index=True)
        save_data(df)
        
        df = df[df['Username'] == username]
        pie_fig, line_fig = create_graphs(df)
        return df.to_dict('records'), pie_fig, line_fig 
    
    @app.callback(
        Output('monthly-progress-bar', 'value'),
        Output('monthly-progress-bar', 'label'),
        Output('monthly-progress-bar', 'color'),
        Output('yearly-progress-bar', 'value'),
        Output('yearly-progress-bar', 'label'),
        Output('yearly-progress-bar', 'color'),
        [Input('save-goals-btn', 'n_clicks'),
        Input('add-expense-button', 'n_clicks')],
        State('monthly-goal-input', 'value'),
        State('yearly-goal-input', 'value'),
    )
    def save_goals(n_clicks_submit, n_clicks, monthly, yearly):
        username = request.cookies.get('username')
        df = load_data()
        df = df[df['Username'] == username]
        if df.empty:
            return 0, "0%", 0, "0%"
        
        goals = load_goals()
        goals[username] = {
            'monthly': monthly if monthly else goals[username]['monthly'],
            'yearly': yearly if yearly else goals[username]['yearly'],
        }
        store_goals(goals)

        return create_goal_graphs(df, username)        
