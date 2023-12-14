from flask import Blueprint, jsonify, make_response, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from forms.login_form import LoginForm
from models import User, Logging
from extensions import db
from flask import session
from functools import wraps
from flask import request
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import logging
from datetime import datetime

auth_logger = logging.getLogger("auth_logger")
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def set_audit_log(user_id, action):
    username = User.query.filter_by(id=user_id).first().username
    
    print(f"Logging action: {action} for user {username}")
    audit_log = Logging()
    audit_log.timestamp = datetime.now()
    audit_log.level = 'INFO'
    audit_log.user_id = user_id
    audit_log.username = username
    audit_log.message = f"User {username} | {action}"
    db.session.add(audit_log)
    db.session.commit()
    print(f"Logging action: {action} for user {username} done")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    timestamp = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_ip = request.remote_addr
    
    auth_logger.info(f"Login attempt from {user_ip} at {timestamp}")
       
    form = LoginForm()
    print(f"Form: {form}")  # Debug print
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            set_audit_log(user.id, 'login')
            
            print("=============================================================")
            print(f"Login successful")
            print(f"User: {user.username}")
            print(f"Password: {form.password.data}")
            print("=============================================================")

            username = form.username.data            
            access_token = create_access_token(identity=username)
            response = make_response(redirect(url_for('main.login_success')))
            response.set_cookie('access_token_cookie', access_token, httponly=True)
            return response
        
        flash('Invalid username or password')
    print(form.errors)
    print(form.username.data)
    print(f"PW: {form.password.data}")
    print("Login failed")
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    response = make_response(redirect(url_for('auth.login')))
    unset_jwt_cookies(response)  # Diese Funktion entfernt die JWT-Cookies
    logout_user()  # Flask-Login's logout_user Funktion aufrufen, falls verwendet
    return response

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'auth_token' not in session:
            return redirect(url_for('login', next=request.url))
        # Token validation logic here
        return f(*args, **kwargs)
    return decorated_function


def generate_auth_token(user_id):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(user_id, salt=current_app.config['SECURITY_PASSWORD_SALT'])