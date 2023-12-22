from flask import Blueprint, jsonify, make_response, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from forms.login_form import LoginForm
from models import User, Logging, LoginAttempt, Role, UserRole
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
from flask_jwt_extended import verify_jwt_in_request

auth_logger = logging.getLogger("auth_logger")
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def jwt_required_optional(fallback_endpoint='auth.login'):
    """Ein Dekorator, der prüft, ob ein gültiges JWT-Cookie vorhanden ist. 
    Leitet zu einer alternativen Seite um, wenn das Cookie fehlt."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                return f(*args, **kwargs)
            except Exception as e:
                return redirect(url_for(fallback_endpoint))

        return decorated_function

    return decorator


def set_audit_log(user_id: int = -1, action: str = "Unknown action") -> None:
    """
        Sets an audit log entry for the given user_id and action
        
        :param user_id: The user_id of the user who performed the action
        :param action: The action that was performed
        
        :return: None
    """
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
def login() -> str:
    """
    Login route for the application. Checks if the user exists and if the password is correct.
    
    :return: The login template or the login_success template if the login was successful, otherwise the user is redirected to the login template
    """
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
                role = db.session.query(Role).join(UserRole).filter(UserRole.user_id == user.id).first()
                access_token = create_access_token(identity=user.id, additional_claims={'role': role.id, 'username': user.username})
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
@jwt_required_optional()
def logout() -> str:
    print("Logout")  # Debug print
    print(f"JWT: {get_jwt_identity()} with role {get_jwt_identity()['role']}")  # Debug print
    response = make_response(redirect(url_for('auth.login')))
    unset_jwt_cookies(response, 'access_token_cookie')
    logout_user()  # Flask-Login's logout_user Funktion aufrufen, falls verwendet
    response.set_cookie('access_token_cookie', '', expires=0)  # Setzt den Cookie manuell auf ein abgelaufenes Datum
    return response


def token_required(f: object) -> object:
    """
    Decorator function to require a valid authentication token.

    This decorator can be used to protect routes that require authentication.
    It checks if the 'auth_token' is present in the session and redirects to the login page if not.
    If the token is present, it performs token validation logic before executing the decorated function.

    Args:
        f: The function to be decorated.

    Returns:
        The decorated function.

    """
    @wraps(f)
    def decorated_function(*args, **kwargs) -> object:
        if 'auth_token' not in session:
            return redirect(url_for('login', next=request.url))
        # Token validation logic here
        return f(*args, **kwargs)
    return decorated_function


def generate_auth_token(user_id: int = -1) -> str:
    if user_id == -1:
        return None
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(user_id, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def log_login_attempt(u_id: int = -1, success: bool = False) -> None:
    """
        Logs the login attempt for the given user_id and success
        
        :param u_id: The user_id of the user who performed the action
        :param success: Whether the login attempt was successful or not
        
        :return: None
    """
    if u_id == -1:
        return None
    values = {'u_id': u_id, 'attempt_time': datetime.now(), 'success': success}
    sql_query = text("INSERT INTO login_attempts (u_id, attempt_time, success) VALUES (:u_id, :attempt_time, :success)")
    db.session.execute(sql_query, values)
    db.session.commit()

def check_login_attempts(u_id, max_attempts_before_penalty, initial_penalty_time, incremental_penalty, max_penalty_time) -> tuple:
    """
        Checks if the user is allowed to login or not
        
        :param u_id: The user_id of the user who performed the action
        :param max_attempts_before_penalty: The maximum number of failed login attempts before the user gets penalized
        :param initial_penalty_time: The initial penalty time in seconds
        :param incremental_penalty: The incremental penalty time in seconds
        :param max_penalty_time: The maximum penalty time in seconds
        
        :return: A tuple containing a boolean indicating whether the user is allowed to login and the time left until the user can login again
    """
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

