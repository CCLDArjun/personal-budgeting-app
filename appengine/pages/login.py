import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from flask import request, make_response
import pickle
import os

dash.register_page(__name__, path='/login')

layout = html.Div([
    html.H2("Login / Signup", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Username"),
        dcc.Input(id='username', type='text', placeholder='Enter your username', style={'width': '100%'}),
        
        html.Label("Password"),
        dcc.Input(id='password', type='password', placeholder='Enter your password', style={'width': '100%'}),
        
        html.Div([
            html.Button('Login', id='login-btn', n_clicks=0, style={'marginRight': '10px'}),
            html.Button('Signup', id='signup-btn', n_clicks=0)
        ], style={'marginTop': '20px'})
        
    ], style={
        'width': '300px',
        'margin': '0 auto',
        'padding': '20px',
        'border': '1px solid #ccc',
        'borderRadius': '10px',
        'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)'
    }),

    html.Div(id='login-message', style={'textAlign': 'center', 'marginTop': '20px'})
])

USER_DB_FILE = 'users.pkl'

def load_users():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_users(users):
    with open(USER_DB_FILE, 'wb') as f:
        pickle.dump(users, f)

def register_callbacks(app):
    # Flask route to set a cookie (used for login)
    @app.server.route('/set-cookie/<username>')
    def set_cookie(username):
        from flask import make_response, redirect
        resp = make_response(redirect('/'))  # redirect to homepage
        resp.set_cookie('username', username)
        return resp

    @app.callback(
        Output('login-message', 'children'),
        [Input('login-btn', 'n_clicks'),
         Input('signup-btn', 'n_clicks')],
        [State('username', 'value'),
         State('password', 'value')],
        prevent_initial_call=True
    )
    def handle_auth(login_clicks, signup_clicks, username, password):
        ctx = dash.callback_context
        if not username or not password:
            return "Username and password are required."

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        users = load_users()

        if button_id == 'signup-btn':
            if username in users:
                return "Username already exists."
            users[username] = password
            save_users(users)
            return "Signup successful. You can now log in."

        elif button_id == 'login-btn':
            if users.get(username) == password:
                # Provide a link to trigger the cookie-setting route
                return html.Div([
                    html.Span(f"Welcome back, {username}! "),
                    dcc.Location(id='redirect-login', href=f'/set-cookie/{username}', refresh=True)
                ])
            else:
                return "Invalid username or password."