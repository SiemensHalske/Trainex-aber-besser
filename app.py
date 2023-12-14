import os
import signal
from flask import Flask, request
from extensions import db, login_manager
from blueprints.auth import auth_bp
from blueprints.main import main_bp
from models import User, db
from sqlalchemy.orm import Session
import os
import logging
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import JWTManager
from waitress import serve
from prometheus_flask_exporter import PrometheusMetrics

log_path = '.\\logs\\app.log'

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

# Configure logging
def init_logging(name: str, log_path: str):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name)
    handler = RotatingFileHandler(log_path, maxBytes=10000000, backupCount=5)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def generate_secret_key(length=24):
    # Generates a secret key
    return os.urandom(length)


def generate_salt(length=24):
    # Generates a salt
    return os.urandom(length).hex()

app = Flask(__name__)
app.config['SECRET_KEY'] = generate_secret_key()
app.config['SECURITY_PASSWORD_SALT'] = generate_salt()
app.config['JWT_SECRET_KEY'] = generate_secret_key()

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

jwt = JWTManager(app)

# database/users.db
database = 'database/educampus.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.path.dirname(__file__), database)}'

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        session = Session(bind=db.engine)
        return session.get(User, int(user_id))
    
@app.before_request
def before_request():
    """
    Log information about incoming requests for debugging purposes.
    """
    print("=============================================================")
    print("Incoming Request:")
    print(f"Remote address: {request.remote_addr}")
    print(f"Method: {request.method}")
    print(f"Path: {request.path}")
    print(f"Headers: {request.headers}")
    print(f"Data: {request.get_data(as_text=True)}")
    print("=============================================================")
    # You can add more information to log as needed

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# Register blueprints
# Register blueprintsk
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(main_bp)


def signal_handler(signal, frame):
    # Fetch the shortcut CTRL+ALT+^
    print('You pressed Ctrl+{0}'.format(signal))
    print('Exiting...')
    exit(0)
    

def initialize_logging():
    
    # Initialize logging
    for key, value in Config.log_dict.items():
        init_logging(key+"_logger", value)


if __name__ == '__main__':
    with app.app_context():
        # Erstellt die Tabellen, wenn sie noch nicht existieren.
        db.create_all()

    host_ip = '0.0.0.0'
    port = 8000

    trigger = signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+{0} to exit'.format(trigger))
    
    cert_path = None
    key_path = None

    ssl_context = ('pfad/zum/zertifikat.crt', 'pfad/zum/private/key.key')

    app.run(debug=True, host=host_ip, port=port)
    
    # serve(app, host=host_ip, port=port, url_scheme='https', threads=4)
