import datetime
from faker import Faker
import random
from create_ibolcdb import (
    Address,
    Branch,
    Country,
    session,
    State,
    Student
    )

fake = Faker()
# Seed the generator for reproducible tests
fake.seed(31415)
random.seed(27182)


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
        state=state_rows[random.randrange(0, num_states)],
        zipcode=fake.postcode()
    )
    return address

TOTAL_STUDENTS = 300
def make_fake_student():
    country = country_rows[random.randrange(0, num_countries)]
    branch = branch_rows[random.randrange(0, num_branches)]

    stud = Student(
        first_name=fake.first_name_male(),
        middle_name=random.choice([fake.first_name_male(), None]),
        last_name=fake.last_name_male(),
        ssn=make_fake_ssn(),
        dob=make_fake_dob(),
        country=country,
        address_id=random.randint(1, TOTAL_STUDENTS),
        cell_phone=fake.phone_number(),
        email=fake.email(),
        branch=branch,
    )
    return stud


def main():
    for i in range(TOTAL_STUDENTS):
        addy = make_fake_address()
        session.add(addy)
    session.commit()

    for i in range(TOTAL_STUDENTS):
        stud = make_fake_student()
        session.add(stud)
    session.commit()

if __name__ == '__main__':
    main()
