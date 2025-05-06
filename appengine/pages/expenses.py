import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from components.expenses_components import (
    load_data, 
    get_category_options, 
    get_table_columns,
    register_expenses_callbacks,
    create_graphs
)
from flask import request

dash.register_page(__name__, path='/expenses')

# Layout
def layout():
    username = request.cookies.get('username')
    if not username:
        return html.Div([
            html.H2("Please login to access this page.", className='text-center my-4'),
        ])
    df = load_data()
    df = df[df['Username'] == username]
    total_spent = df['Amount'].sum()
    avg_spent = df['Amount'].mean()
    pie_fig, line_fig = create_graphs(df)
    
    return html.Div([
        html.H1(f'Expenses Tracker for {username}', className='text-center my-4'),
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
            dbc.Col(dcc.Graph(id='pie-chart', figure=pie_fig), width=6),
            dbc.Col(dcc.Graph(id='line-chart', figure=line_fig), width=6),
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
                        dbc.Input(type='text', id='expense-category')
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
            data=df[df['Username'] == username].to_dict('records'),
            columns=get_table_columns(),
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
            sort_action='native',
            filter_action='native',
            page_size=10
        )
    ])

def register_callbacks(app):
    register_expenses_callbacks(app)
