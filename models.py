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
    roles = db.relationship(
        'Role', secondary='user_role', back_populates='users')
    logs = db.relationship('Logging', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user(username: str = None, uid: int = None):
        user = None

        if username is not None:
            user = User.query.filter_by(username=username).first()
        elif uid is not None:
            user = User.query.filter_by(id=uid).first()

        return user

    def get_uid(username: str = None, email: str = None):
        """Returns the uid of the user with the given username or email"""
        
        user = None

        if username is not None:
            user = User.query.filter_by(username=username).first()
        elif email is not None:
            user = User.query.filter_by(email=email).first()

        return user.id

    def get_username(uid: int = None, email: str = None):
        """Returns the username of the user with the given uid or email"""
        
        user = None

        if uid is not None:
            user = User.query.filter_by(id=uid).first()
        elif email is not None:
            user = User.query.filter_by(email=email).first()

        return user.username
    
    def get_email(uid: int = None, username: str = None):
        """Returns the email of the user with the given uid or username"""
        
        user = None

        if uid is not None:
            user = User.query.filter_by(id=uid).first()
        elif username is not None:
            user = User.query.filter_by(username=username).first()

        return user.email
    
    def get_full_name(uid: int = None, username: str = None) -> str:
        """Returns the full name of the user with the given uid or username"""
        
        user = None

        if uid is not None:
            user = User.query.filter_by(id=uid).first()
        elif username is not None:
            user = User.query.filter_by(username=username).first()

        return user.first_name + ' ' + user.last_name
    
    def get_first_name(uid: int = None, username: str = None):
        """Returns the first name of the user with the given uid or username"""
        
        if uid is not None and username is None:
            first_name = User.get_full_name(uid=uid).split(' ')[0]
        elif username is not None and uid is None:
            first_name = User.get_full_name(username=username).split(' ')[0]
            
        return first_name
    
    def get_last_name(uid: int = None, username: str = None):
        """Returns the last name of the user with the given uid or username"""
        
        if uid is not None and username is None:
            last_name = User.get_full_name(uid=uid).split(' ')[1]
        elif username is not None and uid is None:
            last_name = User.get_full_name(username=username).split(' ')[1]
            
        return last_name        

    def has_role(self, role):
        return role in self.roles

    def __repr__(self):
        return f'<User {self.username}>'


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship(
        'User', secondary='user_role', back_populates='roles')

    def __repr__(self):
        return f'<Role {self.name}>'
    
    def get_role_id(role_name: str):
        """Returns the role id of the role with the given name"""
        
        role = Role.query.filter_by(name=role_name).first()
        return role.id
    
    def get_role_name(role_id: int):
        """Returns the role name of the role with the given id"""
        
        role = Role.query.filter_by(id=role_id).first()
        return role.name
    
    def get_role_names():
        """Returns a list of all role names"""
        
        roles = Role.query.all()
        role_names = []
        
        for role in roles:
            role_names.append(role.name)
            
        return role_names
    
    def get_role_ids():
        """Returns a list of all role ids"""
        
        roles = Role.query.all()
        role_ids = []
        
        for role in roles:
            role_ids.append(role.id)
            
        return role_ids


class UserRole(db.Model):
    __tablename__ = 'user_role'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)

    def __repr__(self):
        return f'<UserRole {self.user_id} {self.role_id}>'
    
    def get_role_ids(uid: int):
        """Returns a list of role ids for the user with the given uid"""
        
        user_roles = UserRole.query.filter_by(user_id=uid).all()
        role_ids = []
        
        for user_role in user_roles:
            role_ids.append(user_role.role_id)
            
        return role_ids
    
    def get_role_names(uid: int):
        """Returns a list of role names for the user with the given uid"""
        
        user_roles = UserRole.query.filter_by(user_id=uid).all()
        role_names = []
        
        for user_role in user_roles:
            role_names.append(Role.get_role_name(user_role.role_id))
            
        return role_names
    
    def get_uid(role_id: int):
        """Returns the uid of the user with the given role id"""
        
        user_role = UserRole.query.filter_by(role_id=role_id).first()
        return user_role.user_id


class Lecturer(db.Model):
    __tablename__ = 'lecturer'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    courses = db.relationship('Course', back_populates='lecturer')

    def __repr__(self):
        return f'<Lecturer {self.first_name} {self.last_name}>'

    def get_lecturer_id(first_name: str, last_name: str):
        """Returns the lecturer id of the lecturer with the given first and last name"""
        
        lecturer = Lecturer.query.filter_by(first_name=first_name, last_name=last_name).first()
        return lecturer.id
    
    def get_lecturer_name(lecturer_id: int):
        """Returns the lecturer name of the lecturer with the given id"""
        
        lecturer = Lecturer.query.filter_by(id=lecturer_id).first()
        return lecturer.first_name + ' ' + lecturer.last_name
    
    def get_lecturer_names():
        """Returns a list of all lecturer names"""
        
        lecturers = Lecturer.query.all()
        lecturer_names = []
        
        for lecturer in lecturers:
            lecturer_names.append(lecturer.first_name + ' ' + lecturer.last_name)
            
        return lecturer_names
    
    def get_lecturer_ids():
        """Returns a list of all lecturer ids"""
        
        lecturers = Lecturer.query.all()
        lecturer_ids = []
        
        for lecturer in lecturers:
            lecturer_ids.append(lecturer.id)
            
        return lecturer_ids
    
    def get_lecturer_email(lecturer_id: int):
        """Returns the email of the lecturer with the given id"""
        
        lecturer = Lecturer.query.filter_by(id=lecturer_id).first()
        return lecturer.email

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

    def __repr__(self):
        return f'<Course {self.title}>'
    
    def get_course_id(title: str):
        """Returns the course id of the course with the given title"""
        
        course = Course.query.filter_by(title=title).first()
        return course.id
    
    def get_course_title(course_id: int):
        """Returns the course title of the course with the given id"""
        
        course = Course.query.filter_by(id=course_id).first()
        return course.title
    
    def get_course_titles():
        """Returns a list of all course titles"""
        
        courses = Course.query.all()
        course_titles = []
        
        for course in courses:
            course_titles.append(course.title)
            
        return course_titles
    
    def get_course_ids():
        """Returns a list of all course ids"""
        
        courses = Course.query.all()
        course_ids = []
        
        for course in courses:
            course_ids.append(course.id)
            
        return course_ids
    
    def get_course_description(course_id: int):
        """Returns the description of the course with the given id"""
        
        course = Course.query.filter_by(id=course_id).first()
        return course.description
    
    def get_course_credit_points(course_id: int):
        """Returns the credit points of the course with the given id"""
        
        course = Course.query.filter_by(id=course_id).first()
        return course.credit_points
    
    def get_course_department(course_id: int):
        """Returns the department of the course with the given id"""
        
        course = Course.query.filter_by(id=course_id).first()
        return course.department.name
    
    def get_course_lecturer(course_id: int):
        """Returns the lecturer of the course with the given id"""
        
        course = Course.query.filter_by(id=course_id).first()
        return course.lecturer.first_name + ' ' + course.lecturer.last_name
    
    def get_course_lecturer_id(course_id: int):
        """Returns the lecturer id of the course with the given id"""
        
        course = Course.query.filter_by(id=course_id).first()
        return course.lecturer_id
    
    def get_courses_for_lecturer(lecturer_id: int):
        """Returns a list of course titles for the lecturer with the given id"""
        
        courses = Course.query.filter_by(lecturer_id=lecturer_id).all()
        course_titles = []
        
        for course in courses:
            course_titles.append(course.title)
            
        return course_titles


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    courses = db.relationship('Course', back_populates='department')

    def __repr__(self):
        return f'<Department {self.name}>'


class Semester(db.Model):
    __tablename__ = 'semester'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Semester {self.name}>'


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', back_populates='events')

    def __repr__(self):
        return f'<Event {self.title}>'


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    room_number = db.Column(db.String(120), nullable=False)
    capacity = db.Column(db.Integer)
    building = db.relationship('Building', back_populates='rooms')
    events = db.relationship('Event', back_populates='room')

    def __repr__(self):
        return f'<Room {self.room_number}>'


class Building(db.Model):
    __tablename__ = 'building'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    story_count = db.Column(db.Integer)
    rooms = db.relationship('Room', back_populates='building')

    def __repr__(self):
        return f'<Building {self.name}>'


class Logging(db.Model):
    __tablename__ = 'logging'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='logs')

    def __repr__(self):
        return f'<Logging {self.level} {self.message}>'
