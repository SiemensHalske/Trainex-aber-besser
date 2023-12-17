from faker import Faker
from sqlalchemy import create_engine, Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random
import re

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

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    event_type_id = Column(Integer, ForeignKey('event_type.id'))
    title = Column(Text, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'))
    room = relationship('Room', back_populates='events')

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def create_fake_event_types(session):
    event_type_names = ['Conference', 'Meeting', 'Lecture', 'Workshop']
    for name in event_type_names:
        event_type = EventType(name=name)
        session.add(event_type)
    session.commit()

def create_fake_rooms(session, number_of_rooms):
    for _ in range(number_of_rooms):
        room_number = f'{random.randint(1, 5)}' + re.sub(r'\D', '', faker.bothify(text='???-###'))
        room = Room(building_id=random.randint(BUILDING_ID_MIN, BUILDING_ID_MAX), room_number=room_number, capacity=random.randint(ROOM_CAPACITY_MIN, ROOM_CAPACITY_MAX))
        session.add(room)
    session.commit()

def create_fake_events(session, number_of_events):
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

def populate_database():
    session = Session()
    create_fake_event_types(session)
    create_fake_rooms(session, NUMBER_OF_ROOMS)
    create_fake_events(session, NUMBER_OF_EVENTS)
    session.close()

if __name__ == "__main__":
    populate_database()
