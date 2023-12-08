import os
import signal
from flask import Flask
from extensions import db, login_manager
from blueprints.auth import auth_bp
from blueprints.main import main_bp
from models import User, db
from sqlalchemy.orm import Session

def generate_secret_key(length=24):
    # Generates a secret key
    return os.urandom(length)

def generate_salt(length=24):
    # Generates a salt
    return os.urandom(length).hex()

app = Flask(__name__)
app.config['SECRET_KEY'] = generate_secret_key()
app.config['SECURITY_PASSWORD_SALT'] = generate_salt()

# C:\Users\Hendrik\Documents\Github\Trainex aber besser\database
database = 'sqlite:///C:\\Users\\Hendrik\\Documents\\Github\\Trainex aber besser\\database\\users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = database

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        session = Session(bind=db.engine)
        return session.get(User, int(user_id))

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


if __name__ == '__main__':
    with app.app_context():
        # This line creates tables if they don't exist already.
        db.create_all()
    host_ip = '0.0.0.0'
    port = 8000
    """
    init the signal handler
    Fetch the shortcut CTRL+ALT+'L'"""
    trigger = signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+{0} to exit'.format(trigger))
    
    app.run(debug=True, host=host_ip, port=port)
