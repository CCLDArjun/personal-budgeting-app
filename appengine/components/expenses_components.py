import dash
from dash import Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import os
import pandas as pd
from google.cloud import storage
import io

USE_GCS = os.environ.get('USE_GCS', '0') == '1'  # Default: use local file


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
        return df
    def save_data(df):
        df.to_csv(DATA_FILE, index=False)

def get_category_options(df):
    return [{'label': c, 'value': c} for c in sorted(df['Category'].unique())]

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

def add_expense(n_clicks, date, category, item, amount):
    if n_clicks is None or not all([date, category, item, amount]):
        return dash.no_update
    df = load_data()
    new_entry = pd.DataFrame([[date, category, item, float(amount)]], columns=["Date", "Category", "Item", "Amount"])
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    return df.to_dict('records')

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
        
        df = load_data()
        new_entry = pd.DataFrame([[date, category, item, float(amount)]], columns=["Date", "Category", "Item", "Amount"])
        df = pd.concat([df, new_entry], ignore_index=True)
        save_data(df)
        
        pie_fig, line_fig = create_graphs(df)
        return df.to_dict('records'), pie_fig, line_fig 