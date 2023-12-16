from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  # Replace with your actual Flask app


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    roles = db.relationship(
        'Role', secondary='user_role', back_populates='users')
    logs = db.relationship('Logging', back_populates='user', foreign_keys='Logging.user_id')  # Add foreign key constraint
    
    login_attempts = db.relationship('LoginAttempt', back_populates='user')
    
    sent_messages = db.relationship('Messages', back_populates='sender', foreign_keys='Messages.u_id1')
    received_messages = db.relationship('Messages', back_populates='recipient', foreign_keys='Messages.u_id2')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    users = db.relationship(
        'User', secondary='user_role', back_populates='roles')


class UserRole(db.Model):
    __tablename__ = 'user_role'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    
    user = db.relationship('User', backref='user_roles')
    role = db.relationship('Role', backref='role_users')


class Lecturer(db.Model):
    __tablename__ = 'lecturer'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    courses = db.relationship('Course', back_populates='lecturer')


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    credit_points = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'))
    department = db.relationship('Department', back_populates='courses')
    lecturer = db.relationship('Lecturer', back_populates='courses')


class Semester(db.Model):
    __tablename__ = 'semester'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', back_populates='events')


class EventType(db.Model):
    __tablename__ = 'event_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class DepartmentBuilding(db.Model):
    __tablename__ = 'department_building'
    department_id = db.Column(db.Integer, db.ForeignKey(
        'department.id'), primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey(
        'building.id'), primary_key=True)
    
    department = db.relationship('Department', back_populates='department_buildings')
    building = db.relationship('Building', back_populates='building_departments')


class Adress(db.Model):
    __tablename__ = 'adress'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.Text, nullable=False)
    zip_code = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    room_number = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer)
    building = db.relationship('Building', back_populates='rooms')
    events = db.relationship('Event', back_populates='room')


class Building(db.Model):
    __tablename__ = 'building'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    story_count = db.Column(db.Integer)
    rooms = db.relationship('Room', back_populates='building')
    building_departments = db.relationship('DepartmentBuilding', back_populates='building')


class Logging(db.Model):
    __tablename__ = 'logging'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='logs')


class LoginAttempt(db.Model):
    __tablename__ = 'login_attempts'
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attempt_time = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    success = db.Column(db.Boolean, nullable=False)

    # Beziehung zu User definieren, um auf User-Objekte zugreifen zu können
    user = db.relationship(
        'User', backref=db.backref('login_attempts', lazy=True))


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    u_id1 = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    u_id2 = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message_timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, nullable=False)
    m_type = db.Column(db.Text, nullable=False)
    subject = db.Column(db.Text, nullable=False)
    
    sender = db.relationship('User', back_populates='sent_messages', foreign_keys=[u_id1])
    recipient = db.relationship('User', back_populates='received_messages', foreign_keys=[u_id2])


class CourseRegistration(db.Model):
    __tablename__ = 'course_registration'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id'), primary_key=True)
    semester_id = db.Column(db.Integer, db.ForeignKey(
        'semester.id'), primary_key=True)

class Resource(db.Model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    r_type = db.Column(db.Text, nullable=False)


class ResourceBooking(db.Model):
    __tablename__ = 'resource_booking'
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey(
        'resource.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    confirmed = db.Column(db.Boolean, nullable=False)
    cancelled = db.Column(db.Boolean, nullable=False)


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    courses = db.relationship('Course', back_populates='department')
    department_buildings = db.relationship('DepartmentBuilding', back_populates='department')


class DepartmentOpeningHours(db.Model):
    __tablename__ = 'department_opening_hours'
    department_id = db.Column(db.Integer, db.ForeignKey(
        'department.id'), primary_key=True)
    opening_hours_id = db.Column(db.Integer, db.ForeignKey(
        'opening_hours.id'), primary_key=True)


class OpeningHours(db.Model):
    __tablename__ = 'opening_hours'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)


class BuildingOpeningHours(db.Model):
    __tablename__ = 'building_opening_hours'
    building_id = db.Column(db.Integer, db.ForeignKey(
        'building.id'), primary_key=True)
    opening_hours_id = db.Column(db.Integer, db.ForeignKey(
        'opening_hours.id'), primary_key=True)

class Archive(db.Model):
    __tablename__ = 'archive'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.LargeBinary, nullable=False)
    archived_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
