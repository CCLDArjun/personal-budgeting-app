import dash
from dash import html, dcc
from flask import request, make_response, redirect

dash.register_page(__name__, path='/logout')

layout = html.Div([
    html.H2("Logging you out..."),
    dcc.Location(id='logout-redirect', href='clear-cookie', refresh=True)
])

def register_callbacks(app):
# Flask route to clear the cookie
    @app.server.route('/clear-cookie')
    def clear_cookie():
        resp = make_response(redirect('/'))  # Redirect to home after logout
        resp.set_cookie('username', '', expires=0)
        return resp
