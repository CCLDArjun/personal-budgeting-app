import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from flask import request
from components.expenses_components import (
    load_data,
    get_category_options,
    get_table_columns,
    register_expenses_callbacks,
    create_graphs
)

dash.register_page(__name__, path='/')

def layout():
    username = request.cookies.get('username')
    if not username:
        return html.Div([
            html.H2([
                "Please ",
                html.A("login", href="/login"),
                " to access this page."
            ], className='text-center my-4')
        ])

    df = load_data()
    df = df[df['Username'] == username]
    total_spent = df['Amount'].sum()
    avg_spent = df['Amount'].mean()
    pie_fig, line_fig = create_graphs(df)

    return html.Div([
        html.H1(f'Expenses Tracker for {username}', className='text-center my-4'),

        # Metrics Cards
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4('Total Spent'),
                    html.H2(id='total-spent-text')
                ])
            ]), width=6),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4('Average Transaction'),
                    html.H2(id='avg-transaction-text')
                ])
            ]), width=6),
        ], className='mb-4'),

        # Graphs
        dbc.Row([
            dbc.Col(dcc.Graph(id='pie-chart', figure=pie_fig), width=6),
            dbc.Col(dcc.Graph(id='line-chart', figure=line_fig), width=6),
        ], className='mb-4'),

        # Goal Setting
        dbc.Card([
            dbc.CardHeader('Set Spending Goals'),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Monthly Spending Limit"),
                        dbc.Input(id='monthly-goal-input', type='number', step='0.01')
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Annual Spending Limit"),
                        dbc.Input(id='yearly-goal-input', type='number', step='0.01')
                    ], width=6),
                ]),
                dbc.Button("Save Goals", id='save-goals-btn', color='success', className='mt-3')
            ])
        ], className='mb-4'),

        # Goal Progress
        dbc.Card([
            dbc.CardHeader("Goal Progress"),
            dbc.CardBody([
                html.H5("Monthly Spending Limit"),
                dbc.Progress(id='monthly-progress-bar', striped=True, animated=True, style={'height': '25px'}),
                html.Br(),
                html.H5("Annual Spending Limit"),
                dbc.Progress(id='yearly-progress-bar', striped=True, animated=True, style={'height': '25px'})
            ])
        ], className='mb-4'),

        # Add Expense
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
                        dbc.Select(id='expense-category', options=get_category_options(None))
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

        # Expenses Table
        dash_table.DataTable(
            id='expenses-table',
            data=df.to_dict('records'),
            columns=get_table_columns(),
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
            sort_action='native',
            filter_action='native',
            page_size=10
        ),
    ])

def register_callbacks(app):
    register_expenses_callbacks(app)
