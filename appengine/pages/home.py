import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.Div([
        html.H1('Your Personal Budgeting Assistant', style={'textAlign': 'center'}),
        html.P([
            "Money Maestro is a personal budgeting app that helps you track your income and expenses. ",
            "It allows you to add, edit, and delete transactions, and view your spending by category. ",
            "It also provides a summary of your total income and expenses, and a chart of your spending by category."
        ]),

    ], style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'padding': '20px',
        'maxWidth': '1200px',
        'margin': '0 auto'
    })
])
