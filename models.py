from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  # Replace with your actual Flask app


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    roles = db.relationship('Role', secondary='user_role', back_populates='users')
    logs = db.relationship('Logging', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', secondary='user_role', back_populates='roles')


class UserRole(db.Model):
    __tablename__ = 'user_role'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)


class Lecturer(db.Model):
    __tablename__ = 'lecturer'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    courses = db.relationship('Course', back_populates='lecturer')


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    credit_points = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'))
    department = db.relationship('Department', back_populates='courses')
    lecturer = db.relationship('Lecturer', back_populates='courses')


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    courses = db.relationship('Course', back_populates='department')


class Semester(db.Model):
    __tablename__ = 'semester'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', back_populates='events')


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    room_number = db.Column(db.String(120), nullable=False)
    capacity = db.Column(db.Integer)
    building = db.relationship('Building', back_populates='rooms')
    events = db.relationship('Event', back_populates='room')


class Building(db.Model):
    __tablename__ = 'building'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    story_count = db.Column(db.Integer)
    rooms = db.relationship('Room', back_populates='building')


class Logging(db.Model):
    __tablename__ = 'logging'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='logs')