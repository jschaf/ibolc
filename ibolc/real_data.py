from .extensions import db
import os

HERE = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(HERE, 'data')


# pylint: disable=no-member
def populate_data_from_script(script):
    script_path = os.path.join(DATA_PATH, script)
    with open(script_path, 'r') as sql_script:
        raw_sql = sql_script.read()
        db.session.execute(raw_sql)
        db.session.commit()


def populate_branches():
    populate_data_from_script('branches.sql')


def populate_countries():
    populate_data_from_script('countries.sql')


def populate_states():
    populate_data_from_script('states.sql')


def populate_mil_components():
    populate_data_from_script('mil_components.sql')


def populate_all():
    populate_branches()
    populate_countries()
    populate_mil_components()
    populate_states()
