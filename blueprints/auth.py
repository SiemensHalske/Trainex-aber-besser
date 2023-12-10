from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from forms.login_form import LoginForm
from models import User, AuditLog
from extensions import db
from flask import session
from functools import wraps
from flask import request
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
import logging

auth_logger = logging.getLogger("auth_logger")

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def set_audit_log(user_id, action):
    print(f"AUDIT LOG - User ID: {user_id}")
    audit_log = AuditLog()
    audit_log.user_id = user_id
    audit_log.action = action
    db.session.add(audit_log)
    db.session.commit()
    print(f"AUDIT LOG - Action: {action}")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    timestamp = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_ip = request.remote_addr
    
    auth_logger.info(f"Login attempt from {user_ip} at {timestamp}")
       
    form = LoginForm()
    print(f"Form: {form}")  # Debug print
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(f"User: {user}")
        print(f"User: {user.username}")
        print(f"User: {user.password_hash}")
        if user and user.check_password(form.password.data):
            login_user(user)
            print("Login successful")
            set_audit_log(user.id, 'login')
            user_id = user.get_UID(form.username.data, None)
            auth_token = generate_auth_token(user_id)
            session['auth_token'] = auth_token
            
            
            return redirect(url_for('main.login_success'))
        flash('Invalid username or password')
    print(form.errors)
    print(form.username.data)
    print(f"PW: {form.password.data}")
    print("Login failed")
    return render_template('login.html', form=form)

def logout_user_token():
    session.pop('auth_token', None)
    logout_user()
    session.clear()

@auth_bp.route('/logout')
def logout():
    logout_user_token()
    return redirect(url_for('auth.login'))

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