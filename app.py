from flask import Flask
from extensions import db, login_manager
from blueprints.auth import auth_bp
from blueprints.main import main_bp
from models import User

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

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(main_bp)

if __name__ == '__main__':
    with app.app_context():
        # This line creates tables if they don't exist already.
        db.create_all()
    app.run(debug=True)
