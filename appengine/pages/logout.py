# logout.py: Handles the logout page and related logic for user sign-out in the budgeting app.
import dash
from dash import html, dcc
from components.login_components import register_logout_routes

dash.register_page(__name__, path='/logout')

layout = html.Div([
    html.H2("Logging you out..."),
    dcc.Location(id='logout-redirect', href='clear-cookie', refresh=True)
])

def register_callbacks(app):
    register_logout_routes(app)
