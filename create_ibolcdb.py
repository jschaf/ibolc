from citext import CIText

from sqlalchemy import (
    Column, Date, DDL, event, Integer, SmallInteger,
    Numeric ,String, create_engine, ForeignKey
)
from sqlalchemy.dialects.postgresql.base import ischema_names
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker, relationship
from sqlalchemy.schema import CreateSchema

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


class Zipcode(types.UserDefinedType):

    def get_col_spec(self):
        return 'zipcode'

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process

ischema_names['zipcode'] = Zipcode


class Email(types.UserDefinedType):

    def get_col_spec(self):
        return 'zipcode'

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process

ischema_names['email'] = Email
Base = automap_base()


event.listen(Base.metadata, 'before_create', CreateSchema('ibolc'))
event.listen(Base.metadata, 'before_create',
             DDL('create extension if not exists citext'))
# TODO: why doesn't the numeric check work
event.listen(Base.metadata, 'before_create',
             DDL("""
             create domain zipcode as text
             constraint zipcode_ck_length_limit check (char_length(value) <= 10)
             constraint zipcode_ck_only_numeric_hyphens check(value ~ '^\d{5}([ \-]?\d{4})?$')
             """))

event.listen(Base.metadata, 'before_create',
             DDL('''
             create domain email as citext
                 constraint email_ck_length
                 check (char_length(value) between 3 and 255)
             '''))

# TODO: create domains for phone_number, zipcode and email

# TODO: add all the column checks

class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    iso = Column(String, nullable=False)
    name = Column(String, nullable=False)
    nice_name = Column(String, nullable=False)
    iso3 = Column(String)
    num_code = Column(SmallInteger)
    phone_code = Column(Numeric(5))

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
    zipcode = Column(Zipcode, nullable=False)
    state = relationship('State')

    def __repr__(self):
        return "<Address({}...)>".format(self.address1[:10])

mil_component_enum = ENUM('Active', 'National Guard', 'Reserve',
                          name='mil_component')
# TODO: add rank


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    last_name = Column(String, nullable=False)
    ssn = Column(SSN, nullable=False)
    dob = Column(Date, nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship('Country')
    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship('Address')
    cell_phone = Column(String)
    email = Column(Email, nullable=False)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': type
    }

    def __repr__(self):
        return "<Person({})>".format(self.last_name)


class Soldier(Person):
    __tablename__ = 'soldier'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    branch_id = Column(Integer, ForeignKey('branch.id'))
    branch = relationship('Branch')
    component = Column('component', mil_component_enum)

    __mapper_args__ = {
        'polymorphic_identity': 'soldier',
    }

    def __repr__(self):
        return "<Soldier({})>".format(self.last_name)


# Python doesn't know about PostGres style inheritance. So we keep it simple and
# pretend like Student is a separate table.
class Student(Soldier):
    __tablename__ = 'student'

    id = Column(Integer, ForeignKey('soldier.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __repr__(self):
        return "<Student({})>".format(self.last_name)


class Cadre(Soldier):
    __tablename__ = 'cadre'

    id = Column(Integer, ForeignKey('soldier.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'cadre',
    }

    def __repr__(self):
        return "<Cadre({})>".format(self.last_name)

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine('postgresql://ibolc@localhost/ibolc')
Session = sessionmaker(bind=engine)
session = Session()
Base.prepare(engine, reflect=True)


def main():
    connection = engine.connect()
    Base.metadata.create_all(engine)
    with open('db/countries.sql', 'r') as countries:
        raw_sql = countries.read()
        connection.execute(raw_sql)

    with open('db/branches.sql', 'r') as branches:
        raw_sql = branches.read()
        connection.execute(raw_sql)

    with open('db/states.sql', 'r') as states:
        raw_sql = states.read()
        connection.execute(raw_sql)

if __name__ == '__main__':
    main()
