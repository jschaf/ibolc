import factory
from factory import Sequence, PostGenerationMethodCall, lazy_attribute
from factory.alchemy import SQLAlchemyModelFactory

import faker

from ibolc import (
    Address, Branch, Cadre, Country, MilComponent, Person, Soldier, State,
    Student
)
from ibolc.user.models import User
from ibolc.database import db

import datetime
import random

fake = faker.Faker()


# The faker SSN provider returns invalid SSNs, like ones that start with 666 or
# are > 900.
def make_fake_ssn():
    area = random.randint(1, 899)
    if area == 666:
        area += 1
    group = random.randint(1, 99)
    serial = random.randint(1, 9999)

    ssn = "{:03d}-{:02d}-{:04d}".format(area, group, serial)
    return ssn


def make_fake_dob(start_year=1950, end_year=1995):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    dob = datetime.date(year, month, day)
    return dob

branch_rows = db.session.query(Branch).all()
country_rows = db.session.query(Country).all()
mil_component_rows = db.session.query(MilComponent).all()
state_rows = db.session.query(State).all()


# pylint: disable=too-few-public-methods
class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db.session


# pylint: disable=W0108
class UserFactory(BaseFactory):
    username = Sequence(lambda n: "user{0}".format(n))
    email = Sequence(lambda n: "user{0}@example.com".format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    active = True

    class Meta:
        model = User


class AddressFactory(BaseFactory):
    address1 = lazy_attribute(lambda n: fake.street_address())
    city = lazy_attribute(lambda n: fake.city())
    state = lazy_attribute(lambda n: random.choice(state_rows))
    zipcode = lazy_attribute(lambda n: fake.postcode())

    class Meta:
        model = Address


class PersonFactory(BaseFactory):

    country = lazy_attribute(lambda n: random.choice(country_rows))
    first_name = lazy_attribute(lambda n: fake.first_name_male())
    middle_name = lazy_attribute(
        lambda n: random.choice([fake.first_name_male(),
                                 None]))
    last_name = lazy_attribute(lambda n: fake.last_name_male())
    ssn = lazy_attribute(lambda n: make_fake_ssn())
    dob = lazy_attribute(lambda n: make_fake_dob())
    country = lazy_attribute(lambda n: random.choice(country_rows))
    address = factory.SubFactory(AddressFactory)
    cell_phone = lazy_attribute(lambda n: fake.phone_number())
    email = lazy_attribute(lambda n: fake.email())
    type = 'person'

    class Meta:
        model = Person


class SoldierFactory(PersonFactory):
    type = 'soldier'
    branch = lazy_attribute(lambda n: random.choice(branch_rows))
    mil_component = lazy_attribute(lambda n: random.choice(mil_component_rows))

    class Meta:
        model = Soldier


class CadreFactory(PersonFactory):
    type = 'cadre'

    class Meta:
        model = Cadre


class StudentFactory(SoldierFactory):
    type = 'student'

    class Meta:
        model = Student


def populate_fake_data():
    StudentFactory.create_batch(300)
    CadreFactory.create_batch(50)

