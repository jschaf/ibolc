#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand

from ibolc import (
    Address, Branch, Cadre, Country, MilComponent, Person, Soldier, State, Student,
)

from ibolc.formation.models import Formation, SoldierFormation
from ibolc.app import create_app
from ibolc.user.models import User
from ibolc.settings import DevConfig, ProdConfig
from ibolc.database import db
from ibolc import real_data


IBOLC_MODELS = [Address, Branch, Cadre, Country, Formation, MilComponent, Person, Soldier,
                SoldierFormation, State, Student, User]


def is_production():
    return os.environ.get('HEROKU') == '1'

if is_production():
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)

def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    context = {'app': app, 'db': db}
    context.update({model.__name__: model for model in IBOLC_MODELS})
    return context

@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

DataManager = Manager(usage="Add and drop data from the database.")


@DataManager.option('-d', '--data-type', dest='data_type', default='all')
def populate(data_type):
    """Fill the database with data, real and fake."""

    from ibolc import factories
    def smart_populate_real_data():
        "Sanity check, don't add data if it already exists."
        if State.query.count() > 0:
            print('Skipping adding real data since it seems to already exist.')
        else:
            real_data.populate_all()

    if data_type == 'all':
        smart_populate_real_data()
        # Must commit real data here so it can be used for the fake data.
        db.session.flush()
        db.session.commit()
        factories.populate_fake_data()
    elif data_type == 'real':
        smart_populate_real_data()
    elif data_type == 'fake':
        factories.populate_fake_data()
    db.session.commit()


@DataManager.command
def delete_all():
    """Remove all rows from the table."""
    # sorted_tables returns tables in foreign key dependency order. That is,
    # each table is preceeded by all tables which it references. But, we need it
    # reveresed to drop the table that depends on the most foreign keys first.
    for table in reversed(db.metadata.sorted_tables):
        rows_deleted = db.session.execute(table.delete()).rowcount
        print("{}: {} rows deleted".format(table.name, rows_deleted))
    db.session.commit()


@DataManager.command
def count():
    for model in IBOLC_MODELS:
        total_rows = model.query.count()
        print("{}: {} rows total".format(model.__name__, total_rows))


@DataManager.command
def create_all():
    """Add all flask models to the database."""
    db.app = app
    db.create_all()

@DataManager.command
def drop_all():
    """Remove all data from the database."""
    db.app = app
    db.drop_all()

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command('data', DataManager)

if __name__ == '__main__':
    manager.run()
