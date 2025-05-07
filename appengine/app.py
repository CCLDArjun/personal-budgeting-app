# app.py: Main entry point for the Dash/Flask budgeting app.
# Sets up the Dash app, navigation, layout, and registers all page callbacks.
from flask import Flask, render_template, request, redirect
import pandas as pd
import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY, '/assets/custom.css'], suppress_callback_exceptions=True)
server = app.server

from pages import expenses
from pages import login
from pages import logout
expenses.register_callbacks(app)
login.register_callbacks(app)
logout.register_callbacks(app)

DATA_FILE = '/data/spending.csv'

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Login", href="/login")),
        dbc.NavItem(dbc.NavLink("Logout", href="/logout")),

    ],
    brand=html.Span("Money Maestro", style={'fontSize': '24px', 'fontWeight': 'bold'}),
    brand_href="/",
    color="dark",
    dark=True,
)

footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(html.Div([
                html.A("GitHub", href="https://github.com/CCLDArjun/personal-budgeting-app", target="_blank"),
                html.Span(" | © 2025 CS122 Group 5")
            ], style={'textAlign': 'center', 'padding': '10px'}))
        ]
    ),
    className="footer",
    fluid=True,
)

app.layout = html.Div([
    navbar,
    html.Div(style={'height': '20px'}),
    dash.page_container,
    footer,
])

if __name__ == '__main__':
    app.run(debug=True)
