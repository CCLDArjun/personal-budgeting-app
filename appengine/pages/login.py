import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from components.login_components import register_login_routes

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

def register_callbacks(app):
    register_login_routes(app)
