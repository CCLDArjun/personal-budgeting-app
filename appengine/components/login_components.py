from flask import redirect, make_response
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash
import pickle
import os
import pandas as pd
from google.cloud import storage
import io

USE_GCS = os.environ.get('USE_GCS', '0') == '1'  # Default: use local file

if USE_GCS:
    BUCKET_NAME = 'cs122-group5.appspot.com'
    USERS_BLOB_NAME = 'users.pkl'
    
    def load_users():
        try:
            client = storage.Client()
            bucket = client.bucket(BUCKET_NAME)
            blob = bucket.blob(USERS_BLOB_NAME)
            data = blob.download_as_bytes()
            return pickle.loads(data)
        except Exception:
            # If file doesn't exist or other error, return empty DataFrame
            return pd.DataFrame(columns=['username', 'password'])

    def save_users(users_df):
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(USERS_BLOB_NAME)
        blob.upload_from_string(pickle.dumps(users_df), content_type='application/octet-stream')
else:
    USER_DB_FILE = 'data/users.pkl'
    
    def load_users():
        if os.path.exists(USER_DB_FILE):
            with open(USER_DB_FILE, 'rb') as f:
                return pickle.load(f)
        return pd.DataFrame(columns=['username', 'password'])

    def save_users(users_df):
        with open(USER_DB_FILE, 'wb') as f:
            pickle.dump(users_df, f)

def check_user_password(username, password, users):
    return username in users and users[username] == password

def register_user(username, password, users):
    users[username] = password
    return users

def register_logout_routes(app):
    @app.server.route('/clear-cookie')
    def clear_cookie():
        resp = make_response(redirect('/'))  # Redirect to home after logout
        resp.set_cookie('username', '', expires=0)
        return resp

def register_login_routes(app):
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
            register_user(username, password, users)
            save_users(users)
            return "Signup successful. You can now log in."

        elif button_id == 'login-btn':
            if check_user_password(username, password, users):
                # Provide a link to trigger the cookie-setting route
                return html.Div([
                    html.Span(f"Welcome back, {username}! "),
                    dcc.Location(id='redirect-login', href=f'/set-cookie/{username}', refresh=True)
                ])
            else:
                return "Invalid username or password."
