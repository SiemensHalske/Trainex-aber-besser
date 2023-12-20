from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  # Replace with your actual Flask app


class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        password_hash (str): The hashed password of the user.
        email (str): The email address of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        is_active (bool): Indicates if the user is active.
        is_admin (bool): Indicates if the user is an admin.
        roles (list): The roles assigned to the user.
        logs (list): The logging entries associated with the user.
        login_attempts (list): The login attempts made by the user.
        sent_messages (list): The messages sent by the user.
        received_messages (list): The messages received by the user.

    Methods:
        set_password(password): Sets the password for the user.
        check_password(password): Checks if the provided password matches the user's password.
    """
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
    logs = db.relationship('Logging', back_populates='user',
                           foreign_keys='Logging.user_id')  # Add foreign key constraint

    login_attempts = db.relationship('LoginAttempt', back_populates='user')

    sent_messages = db.relationship(
        'Messages', back_populates='sender', foreign_keys='Messages.u_id1')
    received_messages = db.relationship(
        'Messages', back_populates='recipient', foreign_keys='Messages.u_id2')

    def set_password(self, password):
        """
        Sets the password for the user.

        Args:
            password (str): The password to set.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the provided password matches the user's password.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    """
    Represents a role in the system.

    Attributes:
        id (int): The unique identifier of the role.
        name (str): The name of the role.
        users (list): The users assigned to the role.
    """
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    users = db.relationship(
        'User', secondary='user_role', back_populates='roles')


class UserRole(db.Model):
    """
    Represents the relationship between users and roles.

    Attributes:
        user_id (int): The ID of the user.
        role_id (int): The ID of the role.

    Relationships:
        user (User): The user associated with the user role.
        role (Role): The role associated with the user role.
    """
    __tablename__ = 'user_role'
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)

    user = db.relationship('User', backref='user_roles',
                           overlaps="roles,users")
    role = db.relationship('Role', backref='role_users')


class Lecturer(db.Model):
    """
    Represents a lecturer in the system.

    Attributes:
        id (int): The unique identifier of the lecturer.
        first_name (str): The first name of the lecturer.
        last_name (str): The last name of the lecturer.
        email (str): The email address of the lecturer.
        courses (list): The courses taught by the lecturer.
        events (list): The events associated with the lecturer.
    """
    __tablename__ = 'lecturer'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    courses = db.relationship('Course', back_populates='lecturer')
    events = db.relationship('Event', back_populates='lecturer')


class Course(db.Model):
    """
    Represents a course in the system.

    Attributes:
        id (int): The unique identifier of the course.
        title (str): The title of the course.
        description (str): The description of the course.
        credit_points (int): The credit points of the course.
        department_id (int): The ID of the department the course belongs to.
        lecturer_id (int): The ID of the lecturer teaching the course.

    Relationships:
        department (Department): The department the course belongs to.
        lecturer (Lecturer): The lecturer teaching the course.
    """
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
    """
    Represents a semester in the system.

    Attributes:
        id (int): The unique identifier of the semester.
        name (str): The name of the semester.
        start_date (datetime): The start date of the semester.
        end_date (datetime): The end date of the semester.
    """
    __tablename__ = 'semester'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)


class Event(db.Model):
    """
    Represents an event in the system.

    Attributes:
        id (int): The unique identifier of the event.
        event_type_id (int): The ID of the event type.
        title (str): The title of the event.
        start_time (datetime): The start time of the event.
        end_time (datetime): The end time of the event.
        description (str): The description of the event.
        room_id (int): The ID of the room where the event takes place.
        lecturer_id (int): The ID of the lecturer associated with the event.

    Relationships:
        room (Room): The room where the event takes place.
        event_type (EventType): The type of the event.
        lecturer (Lecturer): The lecturer associated with the event.
    """
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_type.id'))
    title = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', back_populates='events')
    event_type = db.relationship('EventType', back_populates='events')
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'))
    lecturer = db.relationship('Lecturer', back_populates='events')


class EventType(db.Model):
    """
    Represents an event type in the system.

    Attributes:
        id (int): The unique identifier of the event type.
        name (str): The name of the event type.

    Relationships:
        events (list): The events associated with the event type.
    """
    __tablename__ = 'event_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    events = db.relationship('Event', back_populates='event_type')


class Room(db.Model):
    """
    Represents a room in the system.

    Attributes:
        id (int): The unique identifier of the room.
        building_id (int): The ID of the building the room belongs to.
        room_number (str): The room number.
        capacity (int): The capacity of the room.

    Relationships:
        building (Building): The building the room belongs to.
        events (list): The events taking place in the room.
    """
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    room_number = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer)
    building = db.relationship('Building', back_populates='rooms')
    events = db.relationship('Event', back_populates='room')


class DepartmentBuilding(db.Model):
    """
    Represents the relationship between departments and buildings.

    Attributes:
        department_id (int): The ID of the department.
        building_id (int): The ID of the building.

    Relationships:
        department (Department): The department associated with the department building.
        building (Building): The building associated with the department building.
    """
    __tablename__ = 'department_building'
    department_id = db.Column(db.Integer, db.ForeignKey(
        'department.id'), primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey(
        'building.id'), primary_key=True)

    department = db.relationship(
        'Department', back_populates='department_buildings')
    building = db.relationship(
        'Building', back_populates='building_departments')


class Adress(db.Model):
    """
    Represents an address in the system.

    Attributes:
        id (int): The unique identifier of the address.
        street (str): The street of the address.
        zip_code (str): The ZIP code of the address.
        city (str): The city of the address.
        country (str): The country of the address.
    """
    __tablename__ = 'adress'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.Text, nullable=False)
    zip_code = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)


class Building(db.Model):
    """
    Represents a building in the system.

    Attributes:
        id (int): The unique identifier of the building.
        name (str): The name of the building.
        story_count (int): The number of stories in the building.

    Relationships:
        rooms (list): The rooms in the building.
        address_id (int): The ID of the address associated with the building.
        building_departments (list): The departments associated with the building.
    """
    __tablename__ = 'building'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    story_count = db.Column(db.Integer)
    rooms = db.relationship('Room', back_populates='building')
    address_id = db.Column(db.Integer, db.ForeignKey('adress.id'))
    building_departments = db.relationship(
        'DepartmentBuilding', back_populates='building')


class Logging(db.Model):
    """
    Represents a logging entry in the system.

    Attributes:
        id (int): The unique identifier of the logging entry.
        timestamp (datetime): The timestamp of the logging entry.
        level (str): The level of the logging entry.
        message (str): The message of the logging entry.
        user_id (int): The ID of the user associated with the logging entry.

    Relationships:
        user (User): The user associated with the logging entry.
    """
    __tablename__ = 'logging'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='logs')


class LoginAttempt(db.Model):
    """
    Represents a login attempt in the system.

    Attributes:
        id (int): The unique identifier of the login attempt.
        u_id (int): The ID of the user associated with the login attempt.
        attempt_time (datetime): The time of the login attempt.
        success (bool): Indicates if the login attempt was successful.

    Relationships:
        user (User): The user associated with the login attempt.
    """
    __tablename__ = 'login_attempts'
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attempt_time = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    success = db.Column(db.Boolean, nullable=False)

    user = db.relationship('User', back_populates='login_attempts')


class Messages(db.Model):
    """
    Represents a message in the system.

    Attributes:
        id (int): The unique identifier of the message.
        u_id1 (int): The ID of the sender user.
        u_id2 (int): The ID of the recipient user.
        message_timestamp (datetime): The timestamp of the message.
        message (str): The content of the message.
        read (bool): Indicates if the message has been read.
        m_type (str): The type of the message.
        subject (str): The subject of the message.

    Relationships:
        sender (User): The sender of the message.
        recipient (User): The recipient of the message.
    """
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

    sender = db.relationship(
        'User', back_populates='sent_messages', foreign_keys=[u_id1])
    recipient = db.relationship(
        'User', back_populates='received_messages', foreign_keys=[u_id2])


class CourseRegistration(db.Model):
    """
    Represents a course registration in the system.

    Attributes:
        user_id (int): The ID of the user.
        course_id (int): The ID of the course.
        semester_id (int): The ID of the semester.
    """
    __tablename__ = 'course_registration'
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id'), primary_key=True)
    semester_id = db.Column(db.Integer, db.ForeignKey(
        'semester.id'), primary_key=True)


class Resource(db.Model):
    """
    Represents a resource in the system.

    Attributes:
        id (int): The unique identifier of the resource.
        name (str): The name of the resource.
        r_type (str): The type of the resource.
    """
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    r_type = db.Column(db.Text, nullable=False)


class ResourceBooking(db.Model):
    """
    Represents a resource booking in the system.

    Attributes:
        id (int): The unique identifier of the resource booking.
        resource_id (int): The ID of the resource.
        user_id (int): The ID of the user making the booking.
        start_time (datetime): The start time of the booking.
        end_time (datetime): The end time of the booking.
        room_id (int): The ID of the room where the booking takes place.
        confirmed (bool): Indicates if the booking is confirmed.
        cancelled (bool): Indicates if the booking is cancelled.
    """
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
    """
    Represents a department in the system.

    Attributes:
        id (int): The unique identifier of the department.
        name (str): The name of the department.

    Relationships:
        courses (list): The courses associated with the department.
        department_buildings (list): The department buildings associated with the department.
    """
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    courses = db.relationship('Course', back_populates='department')
    department_buildings = db.relationship(
        'DepartmentBuilding', back_populates='department')


class DepartmentOpeningHours(db.Model):
    """
    Represents the relationship between departments and opening hours.

    Attributes:
        department_id (int): The ID of the department.
        opening_hours_id (int): The ID of the opening hours.
    """
    __tablename__ = 'department_opening_hours'
    department_id = db.Column(db.Integer, db.ForeignKey(
        'department.id'), primary_key=True)
    opening_hours_id = db.Column(db.Integer, db.ForeignKey(
        'opening_hours.id'), primary_key=True)


class OpeningHours(db.Model):
    """
    Represents the opening hours in the system.

    Attributes:
        id (int): The unique identifier of the opening hours.
        day (str): The day of the opening hours.
        start_time (datetime): The start time of the opening hours.
        end_time (datetime): The end time of the opening hours.
        notes (str): Additional notes about the opening hours.
    """
    __tablename__ = 'opening_hours'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)


class BuildingOpeningHours(db.Model):
    """
    Represents the relationship between buildings and opening hours.

    Attributes:
        building_id (int): The ID of the building.
        opening_hours_id (int): The ID of the opening hours.
    """
    __tablename__ = 'building_opening_hours'
    building_id = db.Column(db.Integer, db.ForeignKey(
        'building.id'), primary_key=True)
    opening_hours_id = db.Column(db.Integer, db.ForeignKey(
        'opening_hours.id'), primary_key=True)


class Archive(db.Model):
    """
    Represents an archive entry in the system.

    Attributes:
        id (int): The unique identifier of the archive entry.
        content (bytes): The content of the archive entry.
        archived_date (datetime): The date when the entry was archived.
        course_id (int): The ID of the course associated with the archive entry.
    """
    __tablename__ = 'archive'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.LargeBinary, nullable=False)
    archived_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
