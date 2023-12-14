from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

database_path = '.\\database\\users.db'

db = SQLAlchemy()
login_manager = LoginManager()
