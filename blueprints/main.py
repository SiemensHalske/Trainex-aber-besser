import datetime
import json
import logging

from flask import Blueprint, jsonify, redirect, render_template, abort, url_for
from jinja2 import TemplateNotFound
from flask import session
from functools import wraps
from flask import request
from models import *
from extensions import db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from sqlalchemy import and_
from werkzeug.exceptions import Unauthorized, Forbidden
class Config:
    log_dict = {
        'default': 'logs/default.log',
        'app': 'logs/app.log',
        'auth': 'logs/auth.log',
        'main': 'logs/main.log',
        'models': 'logs/models.log',
        'extensions': 'logs/extensions.log',
        'blueprints': 'logs/blueprints.log',
        'database': 'logs/database.log',
        'forms': 'logs/forms.log',
        'utils': 'logs/utils.log',
        'test': 'logs/test.log',
        'config': 'logs/config.log',
        'templates': 'logs/templates.log',
        'static': 'logs/static.log',
        'migrations': 'logs/migrations.log',
        'logs': 'logs/logs.log',
        'database': 'logs/database.log',
    }


main_logger = logging.getLogger("main_logger")
auth_logger = logging.getLogger("auth_logger")
main_bp = Blueprint('main', __name__)


def get_session_id():
    # Get the user id from the session
    return session.get('user_id', None)


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'auth_token' not in session:
            return redirect(url_for('auth.login', next=request.url))
        # Token validation logic here
        print("Token: %s" % session['auth_token'])
        return f(*args, **kwargs)
    return decorated_function


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    # Redirect to url 'auth.login'
    return redirect(url_for('auth.login'))


@main_bp.route('/login_page', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@main_bp.route('/login_success', methods=['GET', 'POST'])
@jwt_required()
def login_success():
    return render_template('index.html')


@main_bp.route('/get_banner', methods=['GET'])
def get_banner():
    return render_template('banner.html')

# in your main.py or wherever you have your route definitions


@main_bp.route('/banner', methods=['GET', 'POST'], endpoint='banner')
def banner():
    return render_template('banner.html')


@main_bp.route('/aktuelles')
@jwt_required()
def aktuelles():
    return render_template('aktuelles.html')


@main_bp.route('/privates')
@jwt_required()
def privates():
    # Your view logic here
    return render_template('privates.html')


@main_bp.route('/cafe')
@jwt_required()
def cafe():
    # Your view logic here
    return render_template('cafe.html')


@main_bp.route('/learning')
@jwt_required()
def learning():
    # Your view logic here
    return render_template('learning.html')


@main_bp.route('/settings')
@jwt_required()
def settings():
    # Your view logic here
    return render_template('settings.html')


@main_bp.route('/logout_deprecated')
@jwt_required()
def logout():
    # Your view logic here
    session.pop('auth_token', None)
    return render_template('logout.html')


@main_bp.route('/ihk_logo')
def ihk_logo():
    # return the picture
    return render_template('logo.gif')


@main_bp.route('/ihk_logo2')
def ihk_logo2():
    # return the picture
    return render_template('logo2.jpg')


@main_bp.route('/ihk', methods=['GET', 'POST'])
def ihk():
    """Redirect the user to the IHK Nordwest website."""

    return redirect('https://www.ihk-nordwestfalen.de/')


@main_bp.route('/logging', methods=['POST'])
def logging_endpoint():
    """
    Handle logging requests.

    This function receives a JSON payload with logger name, timestamp, and log message, 
    and logs the message using the specified logger.

    The data to be logged is sent in the request body as JSON data.
    Example:
    {
        "logger": "auth",
        "timestamp": "2021-01-01 12:00:00",
        "message": "User xyz logged in"
    }

    Returns:
        JSON: Returns a JSON response with the status of the log operation.
    """

    # Parse JSON data from the request body
    try:
        data = request.json
        desired_logger = data.get('logger', 'default')
        timestamp = data.get('timestamp')
        log_message = data.get('message')
    except json.JSONDecodeError:
        return jsonify({'status': 'error', 'message': 'Invalid JSON data'}), 400

    # Basic validation
    if not log_message or not timestamp:
        return jsonify({'status': 'error', 'message': 'Missing timestamp or message'}), 400

    # Check if the desired logger exists
    if desired_logger not in Config.log_dict:
        return jsonify({'status': 'error', 'message': 'Invalid logger name'}), 400

    # Logging the message
    try:
        logger = logging.getLogger(desired_logger)
        log_message_with_timestamp = f"{timestamp} - {log_message}"
        logger.info(log_message_with_timestamp)
        return jsonify({'status': 'success', 'message': 'Log message recorded'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@main_bp.route('/get_user_info', methods=['GET'])
def get_user_info():
    """
    Retrieves user information based on the provided user ID or email address.

    User ID or email is sent as a query parameter.
    Examples:
    /get_user_info?user_id=1
    /get_user_info?email=test@test.de

    Returns:
        A JSON response containing the user's information.
    """

    user_id = request.args.get('user_id')
    user_email = request.args.get('email')

    if user_id:
        user = User.query.filter_by(id=user_id).first()
    elif user_email:
        user = User.query.filter_by(email=user_email).first()
    else:
        return jsonify({'error': 'No user ID or email provided'}), 400

    if user:
        return jsonify({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'roles': user.roles
        }), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@main_bp.route('/get_user_id', methods=['GET'])
def get_user_id():
    """
    Retrieves the user ID based on the provided username.

    Username is sent as a query parameter.
    Example:
    /get_user_id?user_name=JohnDoe

    Returns:
        A JSON response containing the user ID.
    """
    user_name = request.args.get('user_name')
    if not user_name:
        return jsonify({'error': 'No user name provided'}), 400

    user = User.query.filter_by(username=user_name).first()
    if user:
        return jsonify({'user_id': user.id}), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@main_bp.route('/get_user_name', methods=['GET'])
def get_user_name():
    """
    Get the username of a user based on their user ID.

    User ID is sent as a query parameter.
    Example:
    /get_user_name?user_id=1

    Returns:
        A JSON response containing the user's username.
    """
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'No user ID provided'}), 400

    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify({'user_name': user.username}), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@main_bp.route('/get_user_role', methods=['GET'])
def get_user_role():
    """
    Get the role of a user based on their user ID or email address.

    User ID or email is sent as a query parameter.
    Examples:
    /get_user_role?user_id=1
    /get_user_role?user_email=test1234@gmail.com

    Returns:
        A JSON response containing the user's role.
    """
    user_id = request.args.get('user_id')
    user_email = request.args.get('user_email')

    if user_id:
        user = User.query.filter_by(id=user_id).first()
    elif user_email:
        user = User.query.filter_by(email=user_email).first()
    else:
        return jsonify({'error': 'No user ID or email provided'}), 400

    if user:
        return jsonify({'user_role': user.roles}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# =============================================================
# Calendar endpoints
# =============================================================


@main_bp.route('/calendar_events/', methods=['GET'])
def get_calendar_events():
    """
    Retrieves calendar events for a given user.
    
    Route:
        /calendar_events
        
    Route info:
        - GET: Retrieves calendar events for a given user.
        
    Query string parameters:
        - user_id (int): ID of the user whose events are to be retrieved.
        - lecturer_id (int, optional): ID of the lecturer to filter the events (default: 1).
        
    Example:
        /calendar_events?user_id=1&lecturer_id=1
        
        Retrieves calendar events for user with ID 1 and lecturer with ID 1.
    
        example response:
        [
            {
                "id": 1,
                "title": "Event 1",
                "start_time": "2021-01-01T09:00:00",
                "end_time": "2021-01-01T10:00:00",
                "description": "Event 1 description",
                "lecturer_id": 1
            }
        ]

    Returns:
        A JSON response containing the calendar events for the user.

    Raises:
        400: If the user_id is not provided in the query string parameters.
        500: If an error occurs while fetching the events.
    """
    # Get user_id from the query string parameters
    user_id = get_jwt_identity()
    u_id_valid = User.query.filter_by(id=user_id).first()
    if not user_id or not u_id_valid:
        raise Unauthorized("No user ID provided")

    lecturer_id = request.args.get('lecturer_id', default=1, type=int)

    try:
        # Construct an efficient query
        events = db.session.query(Event).\
            join(Lecturer, Event.lecturer_id == Lecturer.id).\
            join(Course, Lecturer.id == Course.lecturer_id).\
            join(CourseRegistration, and_(Course.id == CourseRegistration.course_id, CourseRegistration.user_id == user_id)).\
            filter(Event.lecturer_id == lecturer_id).\
            all()

        events_data = [{
            'id': event.id,
            'title': event.title,
            'start_time': event.start_time.isoformat(),
            'end_time': event.end_time.isoformat(),
            'description': event.description,
            'lecturer_id': event.lecturer_id,
            # Additional event fields as needed
        } for event in events]
        
        return jsonify(events_data)
    
    except Exception as e:
        # Log the error or send it to a monitoring system
        print(f"An error occurred: {e}")
        error_message = f"An error occurred: {e}"
        error_level = 'ERROR_calender_events'
        log_error(user_id, error_level, error_message)
        return jsonify({"error": "An error occurred fetching events."}), 500


# =============================================================
# Error handlers
# =============================================================

@main_bp.errorhandler(404)
def page_not_found(e: Exception) -> tuple[str, int]:
    return render_template('/error/404.html', error=e), 404


@main_bp.errorhandler(405)
def method_not_allowed(e: Exception) -> tuple[str, int]:
    return render_template('/error/405.html', error=e), 405


@main_bp.errorhandler(500)
def internal_server_error(e: Exception) -> tuple[str, int]:
    return render_template('/error/500.html', error=e), 500


# =============================================================
# Helper functions
# =============================================================

def log_error(user_id = 0, error_level: str = 'INFO', error_message: str = '') -> None:
    """
    Logs an error to the database.
    
    Args:
        error_message (str): The error message to log.
    """
    error_log = Logging()
    error_log.timestamp = datetime.utcnow()
    error_log.level = error_level
    error_log.user_id = user_id
    error_log.message = error_message
    db.session.add(error_log)
    db.session.commit()