import signal
from flask import Flask
from extensions import db, login_manager
from blueprints.auth import auth_bp
from blueprints.main import main_bp
from models import User, db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
# C:\Users\Hendrik\Documents\Github\Trainex aber besser\database
database = 'sqlite:///C:\\Users\\Hendrik\\Documents\\Github\\Trainex aber besser\\database\\users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = database

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    """""
    init the signal handler
    Fetch the shortcut CTRL+ALT+'L'"""
    trigger = signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+{0} to exit'.format(trigger))
    
    app.run(debug=True, host=host_ip, port=port)
