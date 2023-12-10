import logging
from flask import Blueprint, redirect, render_template, abort, url_for
from jinja2 import TemplateNotFound
from flask import session
from functools import wraps
from flask import request

from models import User


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

@main_bp.route('/<page>', methods=['GET', 'POST'])
@token_required
def show(page):
    try:
        return render_template('%s.html' % page)
    except TemplateNotFound:
        abort(404)
        
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
    # Your view logic here
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

@main_bp.route('/logging', methods=['GET', 'POST'])
def logging():
    """
    Handle logging requests.
    
    This function receives a logger name and a log message as query parameters and logs the message using the specified logger.
    
    Args:
        logger (str): The name of the logger to use for logging.
        message (str): The log message to be logged.
    
    Returns:
        int: Returns 1 if the log message was successfully logged, -1 otherwise.
    """
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
    
    desired_logger: str = request.args.get('logger', 'default')
    timestamp: str = request.args.get('timestamp', None)  # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message: str = request.args.get('message', None)
    
    if desired_logger is None:
        return -1
    
    if desired_logger in log_dict:
        logger = logging.getLogger(desired_logger)
        log_message_with_timestamp = f"{timestamp} - {log_message}"
        logger.info(log_message_with_timestamp)
        return 1

@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404