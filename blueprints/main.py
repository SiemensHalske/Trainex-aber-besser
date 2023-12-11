import json
import logging
from flask import Blueprint, jsonify, redirect, render_template, abort, url_for
from jinja2 import TemplateNotFound
from flask import session
from functools import wraps
from flask import request

from models import User
from app import Config


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
@token_required
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
@token_required
def aktuelles():
    return render_template('aktuelles.html')

@main_bp.route('/privates')
@token_required
def privates():
    # Your view logic here
    return render_template('privates.html')

@main_bp.route('/cafe')
@token_required
def cafe():
    # Your view logic here
    return render_template('cafe.html')

@main_bp.route('/learning')
@token_required
def learning():
    # Your view logic here
    return render_template('learning.html')

@main_bp.route('/settings')
@token_required
def settings():
    # Your view logic here
    return render_template('settings.html')	

@main_bp.route('/logout_deprecated')
@token_required
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
        "logger": "app",
        "timestamp": "2021-01-01 12:00:00",
        "message": "This is a log message"
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
    
@main_bp.route('/get_user_id', methods=['GET'])
def get_user_id():
    """
    Retrieves the user ID based on the provided username.
    
    Input data is sent in the request body as JSON data.
    Example:
    {
        "user_name": "John Doe"
    }

    Returns:
        A JSON response containing the user ID.
    """
    data = request.json
    user_name = data.get('user_name')
    user = User.query.filter_by(username=user_name).first()
    return jsonify({'user_id': user.id}), 200

@main_bp.route('/get_user_name', methods=['GET'])
def get_user_name():
    """
    Get the username of a user based on their user ID.
    
    Input data is sent in the request body as JSON data.
    Example:
    {
        "user_id": 1
    }

    Returns:
        A JSON response containing the user's username.
    """
    data = request.json
    user_id = data.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    return jsonify({'user_name': user.username}), 200

@main_bp.route('/get_user_role', methods=['GET'])
def get_user_role():
    """
    Get the role of a user based on their user ID or email address.
    
    Input data is sent in the request body as JSON data.
    Example 1:
    {
        "user_id": 1
    }
    
    Example 2:
    {
        "user_email": "test1234@gmail.com"
    }
    
    Returns:
        A JSON response containing the user's role.
    """
    data = request.json
    
    try:
        user_id = data.get('user_id')
    except json.JSONDecodeError:
        return jsonify({'user_role': 'error'}), 400
    
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        return jsonify({'user_role': user.roles}), 200
    
    try:
        user_email = data.get('user_email')
    except json.JSONDecodeError:
        return jsonify({'user_role': 'error'}), 400
    
    if user_email:
        user = User.query.filter_by(email=user_email).first()
        return jsonify({'user_role': user.roles}), 200
    
    return jsonify({'user_role': 'error'}), 400

@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=e), 404

@main_bp.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html', error=e), 405

@main_bp.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', error=e), 500