from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from config import Config
import requests, json
from models import User, db
from requests.auth import HTTPBasicAuth

auth = Blueprint('auth', __name__, url_prefix='/auth')

# Register Route
@auth.route('/register', methods=('GET', 'POST'))
def register():
    url = Config.API_URL + '/createuser'
    if request.method == 'POST':
        logout_user()
        
        payload = json.dumps({
            "email": request.form['email'],
            "password": request.form['password'],
            "username": request.form['username']
        })
        
        headers = {
            'Content-Type': 'application/json'
            }
        
        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        flash('Account successfully created.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', name='Ecochef')


@auth.route('/login', methods=('GET', 'POST'))
def login():
    url = Config.API_URL + '/login'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        auth = HTTPBasicAuth(username, password)
        response = requests.post(url, auth=auth)
        if response.status_code == 200:
            token = response.json()['token']
            currentUserURL = Config.API_URL + '/currentuser'
            headers = {
            'x-access-token': token
            }
            userResponse = requests.get(currentUserURL, headers=headers)
            if userResponse.status_code == 200:
                userJson = userResponse.json()['user']
                session['user'] = userJson
                session['user']['token'] = token
                # Create session data, we can access this data in other routes
                flash('Login Successful')
            # Redirect to home page
            return redirect(url_for('index'))
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password!')

    return render_template('auth/login.html', name='Ecochef')
   

@auth.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged Out')
    return redirect(url_for('index'))
