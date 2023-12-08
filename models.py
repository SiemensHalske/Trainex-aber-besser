from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  # Replace with your actual Flask app

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', secondary='user_role', back_populates='roles')
    
    def get_role(self, role_id):
        return self.query.filter_by(id=role_id).first()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    roles = db.relationship('Role', secondary='user_role', back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_UID(self, username, email):        
        if username != None:
            return self.query.filter_by(username=username).first().id
        elif email != None:
            return self.query.filter_by(email=email).first().id
        else:
            return -1
    
    def get_username(self, user_id):
        return self.query.filter_by(id=user_id).first().username
    
    def get_email(self, user_id):
        return self.query.filter_by(id=user_id).first().email

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    
    def get_user_role(self, user_id, role_id):
        return self.query.filter_by(user_id=user_id, role_id=role_id).first()
    
    def set_user_role(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id
        db.session.add(self)
        db.session.commit()

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('audit_logs', lazy=True))

    def get_audit_log(self, audit_log_id):
        return self.query.filter_by(id=audit_log_id).first()
    
    def get_audit_logs_by_action(self, action):
        return self.query.filter_by(action=action).all()
    
    def get_audit_logs_by_timestamp(self, timestamp):
        return self.query.filter_by(timestamp=timestamp).all()
    
    def get_audit_logs_by_user(self, user_id):
        return self.query.filter_by(user_id=user_id).all()
    
    def set_audit_log(self, user_id, action):
        self.user_id = user_id
        self.action = action
        db.session.add(self)
        db.session.commit()
        
    def delete_audit_log(self, audit_log_id):
        db.session.delete(self.get_audit_log(audit_log_id))
        
    