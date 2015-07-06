# Python doesn't know about PostGres style inheritance. So we keep it simple and
# pretend like Student is a separate table.



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
