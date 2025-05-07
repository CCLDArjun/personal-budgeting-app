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

# If using GCS, set up the bucket and blob name
# If not, use the local file path
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
        expected_columns = ["Date", "Category", "Item", "Amount", "Username"]
        # Check if file exists and is not empty
        if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
            # Create the file with headers if missing/empty
            pd.DataFrame(columns=expected_columns).to_csv(DATA_FILE, index=False)
            return pd.DataFrame(columns=expected_columns)
        try:
            df = pd.read_csv(DATA_FILE)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=expected_columns)
        df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
        if 'Username' not in df.columns:
            df['Username'] = None
        return df
    def save_data(df):
        df.to_csv(DATA_FILE, index=False)

# Loads and stores user goals
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

# Creates pie and line charts for the expenses page
def create_graphs(df):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df = df[df['Date'].notna()]
    df = df.sort_values('Date')
    category_totals = df.groupby('Category')['Amount'].sum().reset_index()
    pie_fig = px.pie(category_totals, values='Amount', names='Category', title='Spending by Category')
    line_fig = px.line(df, x='Date', y='Amount', title='Spending Over Time')
    return pie_fig, line_fig

# Determines the color of the progress bar based on the progress percentage
def color(progress):
    if progress < 50:
        return 'success'
    elif progress < 80:
        return 'warning'
    else:
        return 'danger'

# Creates the goal graphs for the expenses page
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

# Registers all Dash callbacks related to expenses page (table, charts, progress bars, metrics)
def register_expenses_callbacks(app):
    # Callback to add a new expense and update the table and charts
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
        # Handles adding a new expense and updating the table and charts
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
    
    # Callback to update the monthly and yearly progress bars when goals or expenses change
    @app.callback(
        Output('monthly-progress-bar', 'value'),
        Output('monthly-progress-bar', 'label'),
        Output('monthly-progress-bar', 'color'),
        Output('yearly-progress-bar', 'value'),
        Output('yearly-progress-bar', 'label'),
        Output('yearly-progress-bar', 'color'),
        [
            Input('save-goals-btn', 'n_clicks'),
            Input('add-expense-button', 'n_clicks'),
            Input('expenses-table', 'data'),
        ],
        State('monthly-goal-input', 'value'),
        State('yearly-goal-input', 'value'),
    )
    def save_goals(n_clicks_submit, n_clicks, table_data, monthly, yearly):
        # Handles saving goals and updating progress bars
        username = request.cookies.get('username')
        df = load_data()
        df = df[df['Username'] == username]
        
        goals = load_goals()
        goals[username] = {
            'monthly': monthly if monthly else goals[username]['monthly'],
            'yearly': yearly if yearly else goals[username]['yearly'],
        }
        store_goals(goals)
        
        if df.empty:
            return 0, "0%", "black", 0, "0%", "black"

        return create_goal_graphs(df, username)        

    # Callback to update the total spent and average transaction metrics
    @app.callback(
        Output('total-spent-text', 'children'),
        Output('avg-transaction-text', 'children'),
        Input('expenses-table', 'data')
    )
    def update_metrics(table_data):
        # Updates the total spent and average transaction text
        df = pd.DataFrame(table_data)
        total = df['Amount'].sum() if not df.empty else 0
        avg = df['Amount'].mean() if not df.empty else 0
        return f"${total:.2f}", f"${avg:.2f}"
