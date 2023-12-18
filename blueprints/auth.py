from flask import Blueprint, jsonify, make_response, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from forms.login_form import LoginForm
from models import User, Logging, LoginAttempt
from extensions import db
from flask import session
from functools import wraps
from flask import request
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import logging
from datetime import datetime, timedelta
from sqlalchemy import text

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
    timestamp = datetime.utcnow()
    user_ip = request.remote_addr
    # auth_logger.info(f"Login attempt from {user_ip} at {timestamp}")

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            can_login, time_left = check_login_attempts(
                user.id,
                3,  # Max attempts before penalty
                30,  # Initial penalty time in seconds
                5,   # Incremental penalty time in seconds
                15 * 5  # Max penalty time in seconds
            )
            if not can_login:
                flash(
                    f'Zu viele fehlgeschlagene Loginversuche. Bitte warten Sie {int(time_left)} Sekunden.')
                return render_template('login.html', form=form)

            if user.check_password(form.password.data):
                log_login_attempt(user.id, True)
                access_token = create_access_token(identity=user.id)
                # Stelle sicher, dass 'main_bp.login_success' existiert
                response = make_response(
                    redirect(url_for('main.login_success')))
                response.set_cookie('access_token_cookie',
                                    access_token, httponly=True)
                return response
            else:
                log_login_attempt(user.id, False)
                flash('Ungültiger Benutzername oder Passwort')
        else:
            flash('Ungültiger Benutzername oder Passwort')
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


def log_login_attempt(u_id: int, success: bool):
    values = {'u_id': u_id, 'attempt_time': datetime.now(), 'success': success}
    sql_query = text("INSERT INTO login_attempts (u_id, attempt_time, success) VALUES (:u_id, :attempt_time, :success)")
    db.session.execute(sql_query, values)
    db.session.commit()

def check_login_attempts(u_id, max_attempts_before_penalty, initial_penalty_time, incremental_penalty, max_penalty_time):
    last_attempts = LoginAttempt.query.filter_by(u_id=u_id, success=False) \
                                      .order_by(LoginAttempt.attempt_time.desc()).all()

    # Zählen, wie viele fehlgeschlagene Versuche seit der letzten erfolgreichen Anmeldung gemacht wurden
    attempts_since_last_success = 0
    for attempt in last_attempts:
        if attempt.success:
            break
        attempts_since_last_success += 1

    # Wenn die Anzahl der Versuche geringer ist als das Limit für Strafen, gibt es keine Sperre
    if attempts_since_last_success <= max_attempts_before_penalty:
        return True, None

    # Berechne die aktuelle Sperre basierend auf der Anzahl der Versuche
    penalty_multiplier = min(attempts_since_last_success - max_attempts_before_penalty,
                             (max_penalty_time - initial_penalty_time) // incremental_penalty)
    current_penalty_time = initial_penalty_time + \
        penalty_multiplier * incremental_penalty

    # Überprüfe die Zeit seit dem letzten Versuch
    if last_attempts:
        last_attempt_time = last_attempts[0].attempt_time
        time_since_last_attempt = (
            datetime.now() - last_attempt_time).total_seconds()
        if time_since_last_attempt < current_penalty_time:
            return False, current_penalty_time - time_since_last_attempt


    return True, None
