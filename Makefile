

install:
	pgxn install ssn
	pgxn load -d ibolc ssn

createdb:
	createuser ibolc
	createdb ibolc --encoding=utf8 --owner=ibolc

initdb: addRelations addStateData addCountryData addBranch

connect:
	psql ibolc ibolc

addRelations:
	psql --file=db-init.sql ibolc ibolc

addStateData:
	psql --file=states.sql ibolc ibolc

addCountryData:
	psql --file=countries.sql ibolc ibolc

addBranch:
	psql --file=branches.sql ibolc ibolc

reset:
	psql --file=reset.sql ibolc ibolc
