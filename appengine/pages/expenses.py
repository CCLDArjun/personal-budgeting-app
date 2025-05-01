import dash
from dash import html, dcc, dash_table, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# Register the page for Dash multi-page support
dash.register_page(__name__, path='/expenses')

DATA_FILE = 'data/spending.csv'

# Helper to load data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
    return df

# Layout
def layout():
    df = load_data()
    total_spent = df['Amount'].sum()
    avg_spent = df['Amount'].mean()
    category_totals = df.groupby('Category')['Amount'].sum().reset_index()
    pie_fig = px.pie(category_totals, values='Amount', names='Category', title='Spending by Category')
    line_fig = px.line(df, x='Date', y='Amount', title='Spending Over Time')
    return html.Div([
        html.H1('Expenses Tracker', className='text-center my-4'),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4('Total Spent'),
                    html.H2(f"${total_spent:.2f}")
                ])
            ]), width=6),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4('Average Transaction'),
                    html.H2(f"${avg_spent:.2f}")
                ])
            ]), width=6),
        ], className='mb-4'),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=pie_fig), width=6),
            dbc.Col(dcc.Graph(figure=line_fig), width=6),
        ], className='mb-4'),
        dbc.Card([
            dbc.CardHeader('Add New Expense'),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Date'),
                        dbc.Input(type='date', id='expense-date')
                    ], width=3),
                    dbc.Col([
                        dbc.Label('Category'),
                        dbc.Select(id='expense-category', options=[{'label': c, 'value': c} for c in sorted(df['Category'].unique())])
                    ], width=3),
                    dbc.Col([
                        dbc.Label('Item'),
                        dbc.Input(type='text', id='expense-item')
                    ], width=3),
                    dbc.Col([
                        dbc.Label('Amount'),
                        dbc.Input(type='number', id='expense-amount', step='0.01')
                    ], width=3),
                ]),
                dbc.Button('Add Expense', id='add-expense-button', color='primary', className='mt-3')
            ])
        ], className='mb-4'),
        dash_table.DataTable(
            id='expenses-table',
            data=df.to_dict('records'),
            columns=[
                {'name': 'Date', 'id': 'Date'},
                {'name': 'Category', 'id': 'Category'},
                {'name': 'Item', 'id': 'Item'},
                {'name': 'Amount', 'id': 'Amount', 'type': 'numeric', 'format': {'specifier': '$.2f'}}
            ],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
            sort_action='native',
            filter_action='native',
            page_size=10
        )
    ])

# Callback to add new expense and update table
def register_callbacks(app):
    @app.callback(
        Output('expenses-table', 'data'),
        Input('add-expense-button', 'n_clicks'),
        State('expense-date', 'value'),
        State('expense-category', 'value'),
        State('expense-item', 'value'),
        State('expense-amount', 'value'),
        prevent_initial_call=True
    )
    def add_expense(n_clicks, date, category, item, amount):
        if n_clicks is None or not all([date, category, item, amount]):
            return dash.no_update
        df = load_data()
        new_entry = pd.DataFrame([[date, category, item, float(amount)]], columns=["Date", "Category", "Item", "Amount"])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        return df.to_dict('records')
