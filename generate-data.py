from faker import Faker
from sqlalchemy import Column, Date, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker, relationship
from sqlalchemy.dialects.postgresql.base import ischema_names
from sqlalchemy.dialects.postgresql import ENUM
from citext import CIText

import sqlalchemy.types as types

class SSN(types.UserDefinedType):

    def get_col_spec(self):
        return 'SSN'

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process

ischema_names['ssn'] = SSN
Base = automap_base()


class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    iso = Column(String, nullable=False)
    name = Column(String, nullable=False)
    nice_name = Column(String, nullable=False)
    iso3 = Column(String, nullable=False)
    num_code = Column(Integer, nullable=False)
    phone_code = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Country({})>".format(self.name)

class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    code = Column(String(2), nullable=False)
    name = Column(String, nullable=False)

    def __repr__(self):
        return "<State({})>".format(self.name)

class Branch(Base):
    __tablename__ = 'branch'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    code = Column(String)

    def __repr__(self):
        return "<Branch({})>".format(self.code)

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    address1 = Column(String, nullable=False)
    address2 = Column(String)
    address3 = Column(String)
    city = Column(String, nullable=False)
    state_id = Column(Integer, ForeignKey('state.id'))

    state = relationship('State')

    def __repr__(self):
        return "<Address({}...)>".format(self.address1[:10])

mil_component_enum = ENUM('Active', 'National Guard', 'Reserve',
                          name='mil_component')
# TODO: add rank

class Soldier(Base):
    __tablename__ = 'soldier'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    last_name = Column(String, nullable=False)
    ssn = Column(SSN, nullable=False)
    dob = Column(Date, nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    address_id = Column(Integer, ForeignKey('address.id'))
    cell_phone = Column(String)
    email = Column(CIText, nullable=False)
    branch_id = Column(Integer, ForeignKey('branch.id'))
    component = Column('component', mil_component_enum)

    country = relationship('Country')
    address = relationship('Address')
    branch = relationship('Branch')
    def __repr__(self):
        return "<Soldier({})>".format(self.last_name)

# Python doesn't know about PostGres style inheritance. So we keep it simple and
# pretend like Student is a separate table.
class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    last_name = Column(String, nullable=False)
    ssn = Column(SSN, nullable=False)
    dob = Column(Date, nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    address_id = Column(Integer, ForeignKey('address.id'))
    cell_phone = Column(String)
    email = Column(CIText, nullable=False)
    branch_id = Column(Integer, ForeignKey('branch.id'))

    country = relationship('Country')
    address = relationship('Address')
    branch = relationship('Branch')
    # New things

    def __repr__(self):
        return "<Student({})>".format(self.last_name)


class Cadre(Base):
    __tablename__ = 'cadre'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    last_name = Column(String, nullable=False)
    ssn = Column(SSN, nullable=False)
    dob = Column(Date, nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    address_id = Column(Integer, ForeignKey('address.id'))
    cell_phone = Column(String)
    email = Column(CIText, nullable=False)
    branch_id = Column(Integer, ForeignKey('branch.id'))

    country = relationship('Country')
    address = relationship('Address')
    branch = relationship('Branch')

    # new things

    def __repr__(self):
        return "<Cadre({})>".format(self.last_name)


engine = create_engine('postgresql://ibolc@localhost/ibolc')
Session = sessionmaker(bind=engine)
session = Session()
Base.prepare(engine, reflect=True)


import random
import datetime

fake = Faker()
# Seed the generator for reproducible tests
fake.seed(31415)
random.seed(27182)


def make_fake_dob(start_year=1950, end_year=1995):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    dob = datetime.date(year, month, day)
    return dob

num_countries = session.query(Country).count()
country_rows = session.query(Country).all()

num_branches = session.query(Branch).count()
branch_rows = session.query(Branch).all()

num_states = session.query(State).count()
state_rows = session.query(State).all()

def make_fake_address():
    address = Address(
        address1=fake.street_address(),
        city=fake.city(),
        state=state_rows[random.randrange(0, num_states)]
    )
    return address

def make_fake_student():
    country = country_rows[random.randrange(0, num_countries)]
    branch = branch_rows[random.randrange(0, num_branches)]

    stud = Student(
        first_name=fake.first_name_male(),
        middle_name=random.choice([fake.first_name_male(), None]),
        last_name=fake.last_name_male(),
        ssn=fake.ssn(),
        dob=make_fake_dob(),
        country=country,
        address=make_fake_address(),
        cell_phone=fake.phone_number(),
        email=fake.email(),
        branch=branch,
    )
    return stud


a = make_fake_address()
s = make_fake_student()
