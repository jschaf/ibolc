from sqlalchemy import create_engine, DDL, event
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.schema import CreateSchema


Base = automap_base()

event.listen(Base.metadata, 'before_create', CreateSchema('ibolc'))

event.listen(Base.metadata, 'before_create',
             DDL('create extension if not exists citext'))

event.listen(Base.metadata, 'before_create',
             DDL(r"""
             create domain zipcode as text
             constraint zipcode_ck_length_limit
                 check (char_length(value) <= 10)
             constraint zipcode_ck_only_numeric_hyphens
                 check(value ~ '^\d{5}([ \-]?\d{4})?$')
             """))

event.listen(Base.metadata, 'before_create',
             DDL('''
             create domain email as citext
                 constraint email_ck_length
                 check (char_length(value) between 3 and 255)
             '''))

event.listen(Base.metadata, 'before_create',
             DDL('''
             create domain phone_number as text
             constraint phone_number_ck_length
                check (char_length(value) between 7 and 25)
             '''))

engine = create_engine('postgresql://ibolc@localhost/ibolc')
SessionEngine = sessionmaker(bind=engine)
session = SessionEngine()
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
