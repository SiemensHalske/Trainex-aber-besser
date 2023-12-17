from datetime import datetime
from faker import Faker
from sqlalchemy import LargeBinary, create_engine, Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random
import re
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Boolean
# from models import *

# Konfigurationsvariablen
DB_USERNAME = 'postgres'
DB_PASSWORD = 'zoRRo123'
DB_HOST = 'localhost'
DB_NAME = 'educampus'

DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
NUMBER_OF_ROOMS = 10
NUMBER_OF_EVENTS = 25
ROOM_CAPACITY_MIN = 10
ROOM_CAPACITY_MAX = 100
BUILDING_ID_MIN = 1
BUILDING_ID_MAX = 5

faker = Faker()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True, nullable=False)
    from sqlalchemy import Boolean  # Import the Boolean class from sqlalchemy

    password_hash = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    roles = relationship(
        'Role', secondary='user_role', back_populates='users')
    logs = relationship('Logging', back_populates='user',
                        foreign_keys='Logging.user_id')  # Add foreign key constraint

    login_attempts = relationship('LoginAttempt', back_populates='user')

    sent_messages = relationship(
        'Messages', back_populates='sender', foreign_keys='Messages.u_id1')
    received_messages = relationship(
        'Messages', back_populates='recipient', foreign_keys='Messages.u_id2')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    users = relationship(
        'User', secondary='user_role', back_populates='roles')


class UserRole(Base):
    __tablename__ = 'user_role'
    user_id = Column(Integer, ForeignKey(
        'users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)

    user = relationship('User', backref='user_roles')
    role = relationship('Role', backref='role_users')


class Lecturer(Base):
    __tablename__ = 'lecturer'
    id = Column(Integer, primary_key=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    courses = relationship('Course', back_populates='lecturer')


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    credit_points = Column(Integer)
    department_id = Column(Integer, ForeignKey('department.id'))
    lecturer_id = Column(Integer, ForeignKey('lecturer.id'))
    department = relationship('Department', back_populates='courses')
    lecturer = relationship('Lecturer', back_populates='courses')


class Semester(Base):
    __tablename__ = 'semester'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    event_type_id = Column(Integer, ForeignKey('event_type.id'))
    title = Column(Text, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    description = Column(Text)
    room_id = Column(Integer, ForeignKey('room.id'))
    room = relationship('Room', back_populates='events')
    event_type = relationship('EventType')


class EventType(Base):
    __tablename__ = 'event_type'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)


class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, ForeignKey('building.id'))
    room_number = Column(Text, nullable=False)
    capacity = Column(Integer)
    building = relationship('Building', back_populates='rooms')
    events = relationship('Event', back_populates='room')


class DepartmentBuilding(Base):
    __tablename__ = 'department_building'
    department_id = Column(Integer, ForeignKey(
        'department.id'), primary_key=True)
    building_id = Column(Integer, ForeignKey(
        'building.id'), primary_key=True)

    department = relationship(
        'Department', back_populates='department_buildings')
    building = relationship(
        'Building', back_populates='building_departments')


class Adress(Base):
    __tablename__ = 'adress'
    id = Column(Integer, primary_key=True)
    street = Column(Text, nullable=False)
    zip_code = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    country = Column(Text, nullable=False)


class Building(Base):
    __tablename__ = 'building'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    story_count = Column(Integer)
    rooms = relationship('Room', back_populates='building')
    address_id = Column(Integer, ForeignKey('adress.id'))
    building_departments = relationship(
        'DepartmentBuilding', back_populates='building')


class Logging(Base):
    __tablename__ = 'logging'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(Text, nullable=False)
    message = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='logs')


class LoginAttempt(Base):
    __tablename__ = 'login_attempts'
    id = Column(Integer, primary_key=True)
    u_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    attempt_time = Column(
        DateTime, default=datetime.utcnow, nullable=False)
    success = Column(Boolean, nullable=False)

    # Beziehung zu User definieren, um auf User-Objekte zugreifen zu können
    user = relationship('User', back_populates='login_attempts')


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    u_id1 = Column(Integer, ForeignKey('users.id'), nullable=False)
    u_id2 = Column(Integer, ForeignKey('users.id'), nullable=False)
    message_timestamp = Column(
        DateTime, default=datetime.utcnow, nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, nullable=False)
    m_type = Column(Text, nullable=False)
    subject = Column(Text, nullable=False)

    sender = relationship(
        'User', back_populates='sent_messages', foreign_keys=[u_id1])
    recipient = relationship(
        'User', back_populates='received_messages', foreign_keys=[u_id2])


class CourseRegistration(Base):
    __tablename__ = 'course_registration'
    user_id = Column(Integer, ForeignKey(
        'users.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey(
        'course.id'), primary_key=True)
    semester_id = Column(Integer, ForeignKey(
        'semester.id'), primary_key=True)


class Resource(Base):
    __tablename__ = 'resource'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    r_type = Column(Text, nullable=False)


class ResourceBooking(Base):
    __tablename__ = 'resource_booking'
    id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey(
        'resource.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'))
    confirmed = Column(Boolean, nullable=False)
    cancelled = Column(Boolean, nullable=False)


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    courses = relationship('Course', back_populates='department')
    department_buildings = relationship(
        'DepartmentBuilding', back_populates='department')


class DepartmentOpeningHours(Base):
    __tablename__ = 'department_opening_hours'
    department_id = Column(Integer, ForeignKey(
        'department.id'), primary_key=True)
    opening_hours_id = Column(Integer, ForeignKey(
        'opening_hours.id'), primary_key=True)


class OpeningHours(Base):
    __tablename__ = 'opening_hours'
    id = Column(Integer, primary_key=True)
    day = Column(Text, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    notes = Column(Text)


class BuildingOpeningHours(Base):
    __tablename__ = 'building_opening_hours'
    building_id = Column(Integer, ForeignKey(
        'building.id'), primary_key=True)
    opening_hours_id = Column(Integer, ForeignKey(
        'opening_hours.id'), primary_key=True)


class Archive(Base):
    __tablename__ = 'archive'
    id = Column(Integer, primary_key=True)
    content = Column(LargeBinary, nullable=False)
    archived_date = Column(
        DateTime, default=datetime.utcnow, nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'))


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def create_fake_event_types(session):
    try:
        event_type_names = ['Conference', 'Meeting', 'Lecture', 'Workshop']
        for name in event_type_names:
            event_type = EventType(name=name)
            session.add(event_type)
        session.commit()
    except Exception as e:
        print(f"An error occurred while creating fake event types: {str(e)}")
        session.rollback()
    finally:
        session.close()


def create_fake_rooms(session, number_of_rooms):
    try:
        for _ in range(number_of_rooms):
            room_number = f'{random.randint(1, 5)}' + \
                re.sub(r'\D', '', faker.bothify(text='???-###'))
            room = Room(building_id=random.randint(BUILDING_ID_MIN, BUILDING_ID_MAX),
                        room_number=room_number, capacity=random.randint(ROOM_CAPACITY_MIN, ROOM_CAPACITY_MAX))
            session.add(room)
        session.commit()
    except Exception as e:
        print(f"An error occurred while creating fake rooms: {str(e)}")
        session.rollback()
    finally:
        session.close()


def create_fake_events(session, number_of_events):
    try:
        event_types = session.query(EventType).all()
        rooms = session.query(Room).all()
        for _ in range(number_of_events):
            event = Event(
                event_type_id=random.choice(event_types).id,
                title=faker.sentence(),
                start_time=faker.date_time(),
                end_time=faker.date_time(),
                room_id=random.choice(rooms).id
            )
            session.add(event)
        session.commit()
    except Exception as e:
        print(f"An error occurred while creating fake events: {str(e)}")
        session.rollback()
    finally:
        session.close()

def create_fake_buildings(session, number_of_buildings=5):
    try:
        for _ in range(number_of_buildings):
            building = Building(
                name=faker.company(),
                story_count=random.randint(BUILDING_ID_MIN, BUILDING_ID_MAX),
                address_id=random.randint(1, 1)
            )
            session.add(building)
        session.commit()
    except Exception as e:
        print(f"An error occurred while creating fake buildings: {str(e)}")
        session.rollback()
    finally:
        session.close()


def populate_database():
    session = Session()
    create_fake_event_types(session)
    create_fake_rooms(session, NUMBER_OF_ROOMS)
    create_fake_events(session, NUMBER_OF_EVENTS)
    create_fake_buildings(session)  # Call the create_fake_buildings method
    session.close()


if __name__ == "__main__":
    populate_database()
