from ibolc.branch.models import Branch
from ibolc.cadre.models import Cadre
from ibolc.country.models import Country
from ibolc.person.models import Person
from ibolc.soldier.models import Soldier
from ibolc.student.models import Student
from .extensions import db
import datetime
from faker import Faker
import os
import random

HERE = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(HERE, 'data')


def fill_data_from_script(script):
    script_path = os.path.join(DATA_PATH, script)
    with open(script_path, 'r') as sql_script:
        raw_sql = sql_script.read()
        db.session.execute(raw_sql)
        db.session.commit()


def fill_branches():
    fill_data_from_script('branches.sql')


def fill_countries():
    fill_data_from_script('countries.sql')


def fill_states():
    fill_data_from_script('states.sql')

# fake = Faker()
# # Seed the generator for reproducible tests
# fake.seed(31415)
# random.seed(27182)

# # The faker SSN provider returns invalid SSNs, like ones that start with 666 or
# # are > 900.
# def make_fake_ssn():
#     area = random.randint(1, 899)
#     if area == 666:
#         area += 1
#     group = random.randint(1, 99)
#     serial = random.randint(1, 9999)

#     ssn = "{:03d}-{:02d}-{:04d}".format(area, group, serial)
#     return ssn

# def make_fake_dob(start_year=1950, end_year=1995):
#     year = random.randint(start_year, end_year)
#     month = random.randint(1, 12)
#     day = random.randint(1, 28)
#     dob = datetime.date(year, month, day)
#     return dob

# num_countries = db.engine.query(Country).count()
# country_rows = db.engine.query(Country).all()

# num_branches = db.engine.query(Branch).count()
# branch_rows = db.engine.query(Branch).all()

# num_states = db.engine.query(State).count()
# state_rows = db.engine.query(State).all()

# def make_fake_address():
#     address = Address(
#         address1=fake.street_address(),
#         city=fake.city(),
#         state=state_rows[random.randrange(0, num_states)],
#         zipcode=fake.postcode()
#     )
#     return address

# TOTAL_STUDENTS = 300
# def make_fake_student():
#     country = country_rows[random.randrange(0, num_countries)]
#     branch = branch_rows[random.randrange(0, num_branches)]

#     stud = Student(
#         first_name=fake.first_name_male(),
#         middle_name=random.choice([fake.first_name_male(), None]),
#         last_name=fake.last_name_male(),
#         ssn=make_fake_ssn(),
#         dob=make_fake_dob(),
#         country=country,
#         address=make_fake_address(),
#         cell_phone=fake.phone_number(),
#         email=fake.email(),
#         branch=branch,
#     )
#     return stud


def fill_all():
    fill_branches()
    fill_countries()
    fill_states()

# def main():
#     for i in range(TOTAL_STUDENTS):
#         stud = make_fake_student()
#         db.engine.add(stud)
#     db.engine.commit()

# if __name__ == '__main__':
#     fill_all()
