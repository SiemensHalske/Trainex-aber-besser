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

        lecturer = Lecturer.query.filter_by(
            first_name=first_name, last_name=last_name).first()
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
            lecturer_names.append(lecturer.first_name +
                                  ' ' + lecturer.last_name)

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

    def __repr__(self) -> str:
        return f'<Course {self.title}>'

    def get_course_id(title: str) -> int:
        """Returns the course id of the course with the given title"""

        course = Course.query.filter_by(title=title).first()
        return course.id

    def get_course_title(course_id: int) -> str:
        """Returns the course title of the course with the given id"""

        course = Course.query.filter_by(id=course_id).first()
        return course.title

    def get_course_titles() -> list:
        """Returns a list of all course titles"""

        courses = Course.query.all()
        course_titles = []

        for course in courses:
            course_titles.append(course.title)

        return course_titles

    def get_course_ids() -> list:
        """Returns a list of all course ids"""

        courses = Course.query.all()
        course_ids = []

        for course in courses:
            course_ids.append(course.id)

        return course_ids

    def get_course_description(course_id: int) -> str:
        """Returns the description of the course with the given id"""

        course = Course.query.filter_by(id=course_id).first()
        return course.description

    def get_course_credit_points(course_id: int) -> int:
        """Returns the credit points of the course with the given id"""

        course = Course.query.filter_by(id=course_id).first()
        return course.credit_points

    def get_course_department(course_id: int) -> str:
        """Returns the department of the course with the given id"""

        course = Course.query.filter_by(id=course_id).first()
        return course.department.name

    def get_course_lecturer(course_id: int) -> str:
        """Returns the lecturer of the course with the given id"""

        course = Course.query.filter_by(id=course_id).first()
        return course.lecturer.first_name + ' ' + course.lecturer.last_name

    def get_course_lecturer_id(course_id: int) -> int:
        """Returns the lecturer id of the course with the given id"""

        course = Course.query.filter_by(id=course_id).first()
        return course.lecturer_id

    def get_courses_for_lecturer(lecturer_id: int) -> list:
        """Returns a list of course titles for the lecturer with the given id"""

        courses = Course.query.filter_by(lecturer_id=lecturer_id).all()
        course_titles = []

        for course in courses:
            course_titles.append(course.title)

        return course_titles

    def get_courses_for_department(department_id: int) -> list:
        """Returns a list of course titles for the department with the given id"""

        courses = Course.query.filter_by(department_id=department_id).all()
        course_titles = []

        for course in courses:
            course_titles.append(course.title)

        return course_titles

    def get_courses_for_semester(semester_id: int) -> list:
        """Returns a list of course titles for the semester with the given id"""

        courses = Course.query.filter_by(semester_id=semester_id).all()
        course_titles = []

        for course in courses:
            course_titles.append(course.title)

        return course_titles

    def get_courses_for_student(student_id: int) -> list:
        """Returns a list of course titles for the student with the given id"""

        courses = Course.query.filter_by(student_id=student_id).all()
        course_titles = []

        for course in courses:
            course_titles.append(course.title)

        return course_titles

    def get_courses_for_student_by_semester(student_id: int, semester_id: int) -> list:
        """Returns a list of course titles for the student with the given id and semester id"""

        courses = Course.query.filter_by(
            student_id=student_id, semester_id=semester_id).all()
        course_titles = []

        for course in courses:
            course_titles.append(course.title)

        return course_titles

    def get_course(semester_id: int, title: str) -> any or None:
        """Returns the course with the given semester id and title"""

        course = Course.query.filter_by(
            semester_id=semester_id, title=title).first()
        return course

    def get_course_by_id(course_id: int) -> any or None:
        """Returns the course with the given id"""

        course = Course.query.filter_by(id=course_id).first()
        return course


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    courses = db.relationship('Course', back_populates='department')

    def __repr__(self):
        return f'<Department {self.name}>'

    def get_department_id(name: str) -> int:
        """Returns the department id of the department with the given name"""

        department = Department.query.filter_by(name=name).first()
        return department.id

    def get_department_ids() -> list:
        """Returns a list of all department ids"""

        departments = Department.query.all()
        department_ids = []

        for department in departments:
            department_ids.append(department.id)

        return department_ids

    def get_department_name(department_id: int) -> str:
        """Returns the department name of the department with the given id"""

        department = Department.query.filter_by(id=department_id).first()
        return department.name

    def get_department_names() -> list:
        """Returns a list of all department names"""

        departments = Department.query.all()
        department_names = []

        for department in departments:
            department_names.append(department.name)

        return department_names

    def get_department_courses(department_id: int) -> list:
        """Returns a list of course titles for the department with the given id"""

        department = Department.query.filter_by(id=department_id).first()
        courses = department.courses
        course_titles = []

        for course in courses:
            course_titles.append(course.title)

        return course_titles

    def get_department_courses_by_semester(department_id: int, semester_id: int) -> list:
        """Returns a list of course titles for the department with the given id and semester id"""

        department = Department.query.filter_by(id=department_id).first()
        courses = department.courses
        course_titles = []

        for course in courses:
            if course.semester_id == semester_id:
                course_titles.append(course.title)

        return course_titles

    def get_department_courses_by_lecturer(department_id: int, lecturer_id: int) -> list:
        """Returns a list of course titles for the department with the given id and lecturer id"""

        department = Department.query.filter_by(id=department_id).first()
        courses = department.courses
        course_titles = []

        for course in courses:
            if course.lecturer_id == lecturer_id:
                course_titles.append(course.title)

        return course_titles


class Semester(db.Model):
    __tablename__ = 'semester'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Semester {self.name}>'

    def get_semester_id(name: str) -> int:
        """Returns the semester id of the semester with the given name"""

        semester = Semester.query.filter_by(name=name).first()
        return semester.id

    def get_semester_ids() -> list:
        """Returns a list of all semester ids"""

        semesters = Semester.query.all()
        semester_ids = []

        for semester in semesters:
            semester_ids.append(semester.id)

        return semester_ids

    def get_semester_name(semester_id: int) -> str:
        """Returns the semester name of the semester with the given id"""

        semester = Semester.query.filter_by(id=semester_id).first()
        return semester.name

    def get_semester_names() -> list:
        """Returns a list of all semester names"""

        semesters = Semester.query.all()
        semester_names = []

        for semester in semesters:
            semester_names.append(semester.name)

        return semester_names

    def get_semester_start_date(semester_id: int) -> datetime:
        """Returns the start date of the semester with the given id"""

        semester = Semester.query.filter_by(id=semester_id).first()
        return semester.start_date

    def get_semester_end_date(semester_id: int) -> datetime:
        """Returns the end date of the semester with the given id"""

        semester = Semester.query.filter_by(id=semester_id).first()
        return semester.end_date


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

    def get_event_id(title: str) -> int:
        """Returns the event id of the event with the given title"""

        event = Event.query.filter_by(title=title).first()
        return event.id

    def get_event_ids() -> list:
        """Returns a list of all event ids"""

        events = Event.query.all()
        event_ids = []

        for event in events:
            event_ids.append(event.id)

        return event_ids

    def get_event_title(event_id: int) -> str:
        """Returns the event title of the event with the given id"""

        event = Event.query.filter_by(id=event_id).first()
        return event.title

    def get_event_titles() -> list:
        """Returns a list of all event titles"""

        events = Event.query.all()
        event_titles = []

        for event in events:
            event_titles.append(event.title)

        return event_titles

    def get_event_start_time(event_id: int) -> datetime:
        """Returns the start time of the event with the given id"""

        event = Event.query.filter_by(id=event_id).first()
        return event.start_time

    def get_event_end_time(event_id: int) -> datetime:
        """Returns the end time of the event with the given id"""

        event = Event.query.filter_by(id=event_id).first()
        return event.end_time

    def get_event_description(event_id: int) -> str:
        """Returns the description of the event with the given id"""

        event = Event.query.filter_by(id=event_id).first()
        return event.description

    def get_event_room(event_id: int) -> str:
        """Returns the room of the event with the given id"""

        event = Event.query.filter_by(id=event_id).first()
        return event.room.room_number

    def get_event_room_id(event_id: int) -> int:
        """Returns the room id of the event with the given id"""

        event = Event.query.filter_by(id=event_id).first()
        return event.room_id

    def get_events_for_room(room_id: int) -> list:
        """Returns a list of event titles for the room with the given id"""

        events = Event.query.filter_by(room_id=room_id).all()
        event_titles = []

        for event in events:
            event_titles.append(event.title)

        return event_titles

    def get_events_for_room_by_date(room_id: int, date: datetime) -> list:
        """Returns a list of event titles for the room with the given id and date"""

        events = Event.query.filter_by(room_id=room_id).all()
        event_titles = []

        for event in events:
            if event.start_time.date() == date.date():
                event_titles.append(event.title)

        return event_titles

    def get_events_for_room_by_date_range(room_id: int, start_date: datetime, end_date: datetime) -> list:
        """Returns a list of event titles for the room with the given id and date range"""

        events = Event.query.filter_by(room_id=room_id).all()
        event_titles = []

        for event in events:
            if event.start_time.date() >= start_date.date() and event.start_time.date() <= end_date.date():
                event_titles.append(event.title)

        return event_titles

    def get_events_for_room_by_semester(room_id: int, semester_id: int) -> list:
        """Returns a list of event titles for the room with the given id and semester id"""

        events = Event.query.filter_by(room_id=room_id).all()
        event_titles = []

        for event in events:
            if event.semester_id == semester_id:
                event_titles.append(event.title)

        return event_titles


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

    def get_room_id(room_number: str) -> int:
        """Returns the room id of the room with the given room number"""

        room = Room.query.filter_by(room_number=room_number).first()
        return room.id

    def get_room_ids() -> list:
        """Returns a list of all room ids"""

        rooms = Room.query.all()
        room_ids = []

        for room in rooms:
            room_ids.append(room.id)

        return room_ids

    def get_room_number(room_id: int) -> str:
        """Returns the room number of the room with the given id"""

        room = Room.query.filter_by(id=room_id).first()
        return room.room_number

    def get_room_numbers() -> list:
        """Returns a list of all room numbers"""

        rooms = Room.query.all()
        room_numbers = []

        for room in rooms:
            room_numbers.append(room.room_number)

        return room_numbers

    def get_room_capacity(room_id: int) -> int:
        """Returns the capacity of the room with the given id"""

        room = Room.query.filter_by(id=room_id).first()
        return room.capacity

    def get_room_building(room_id: int) -> str:
        """Returns the building of the room with the given id"""

        room = Room.query.filter_by(id=room_id).first()
        return room.building.name

    def get_room_building_id(room_id: int) -> int:
        """Returns the building id of the room with the given id"""

        room = Room.query.filter_by(id=room_id).first()
        return room.building_id

    def get_rooms_for_building(building_id: int) -> list:
        """Returns a list of room numbers for the building with the given id"""

        rooms = Room.query.filter_by(building_id=building_id).all()
        room_numbers = []

        for room in rooms:
            room_numbers.append(room.room_number)

        return room_numbers


class Building(db.Model):
    __tablename__ = 'building'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    story_count = db.Column(db.Integer)
    rooms = db.relationship('Room', back_populates='building')

    def __repr__(self):
        return f'<Building {self.name}>'

    def get_building_id(name: str) -> int:
        """Returns the building id of the building with the given name"""

        building = Building.query.filter_by(name=name).first()
        return building.id

    def get_building_ids() -> list:
        """Returns a list of all building ids"""

        buildings = Building.query.all()
        building_ids = []

        for building in buildings:
            building_ids.append(building.id)

        return building_ids

    def get_building_name(building_id: int) -> str:
        """Returns the building name of the building with the given id"""

        building = Building.query.filter_by(id=building_id).first()
        return building.name

    def get_building_names() -> list:
        """Returns a list of all building names"""

        buildings = Building.query.all()
        building_names = []

        for building in buildings:
            building_names.append(building.name)

        return building_names

    def get_building_story_count(building_id: int) -> int:
        """Returns the story count of the building with the given id"""

        building = Building.query.filter_by(id=building_id).first()
        return building.story_count

    def get_building_rooms(building_id: int) -> list:
        """Returns a list of room numbers for the building with the given id"""

        building = Building.query.filter_by(id=building_id).first()
        rooms = building.rooms
        room_numbers = []

        for room in rooms:
            room_numbers.append(room.room_number)

        return room_numbers


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

    def get_log_id(timestamp: datetime, level: str, message: str) -> int:
        """Returns the log id of the log with the given timestamp, level, and message"""

        log = Logging.query.filter_by(
            timestamp=timestamp, level=level, message=message).first()
        return log.id

    def get_log_ids() -> list:
        """Returns a list of all log ids"""

        logs = Logging.query.all()
        log_ids = []

        for log in logs:
            log_ids.append(log.id)

        return log_ids

    def get_log_timestamp(log_id: int) -> datetime:
        """Returns the timestamp of the log with the given id"""

        log = Logging.query.filter_by(id=log_id).first()
        return log.timestamp

    def get_log_level(log_id: int) -> str:
        """Returns the level of the log with the given id"""

        log = Logging.query.filter_by(id=log_id).first()
        return log.level

    def get_log_message(log_id: int) -> str:
        """Returns the message of the log with the given id"""

        log = Logging.query.filter_by(id=log_id).first()
        return log.message

    def get_log_user(log_id: int) -> str:
        """Returns the user of the log with the given id"""

        log = Logging.query.filter_by(id=log_id).first()
        return log.user.username

    def get_log_user_id(log_id: int) -> int:
        """Returns the user id of the log with the given id"""

        log = Logging.query.filter_by(id=log_id).first()
        return log.user_id

    def get_logs_for_user(user_id: int) -> list:
        """Returns a list of log ids for the user with the given id"""

        logs = Logging.query.filter_by(user_id=user_id).all()
        log_ids = []

        for log in logs:
            log_ids.append(log.id)

        return log_ids

    def get_logs_for_user_by_date(user_id: int, date: datetime) -> list:
        """Returns a list of log ids for the user with the given id and date"""

        logs = Logging.query.filter_by(user_id=user_id).all()
        log_ids = []

        for log in logs:
            if log.timestamp.date() == date.date():
                log_ids.append(log.id)

        return log_ids


class LoginAttempt(db.Model):
    __tablename__ = 'login_attempts'
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attempt_time = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    success = db.Column(db.Boolean, nullable=False)

    # Beziehung zu User definieren, um auf User-Objekte zugreifen zu können
    user = db.relationship(
        'User', backref=db.backref('login_attempts', lazy=True))

    def __repr__(self):
        return f'<LoginAttempt {self.u_id} {self.attempt_time} {self.success}>'

    def get_login_attempt_id(u_id: int, attempt_time: datetime, success: bool) -> int:
        """Returns the login attempt id of the login attempt with the given user id, attempt time, and success"""

        login_attempt = LoginAttempt.query.filter_by(
            u_id=u_id, attempt_time=attempt_time, success=success).first()
        return login_attempt.id
