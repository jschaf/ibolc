

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
	psql --file=db/init.sql ibolc ibolc

fillData: addStateData addCountryData addBranch

addStateData:
	psql --file=db/states.sql ibolc ibolc

addCountryData:
	psql --file=db/countries.sql ibolc ibolc

addBranch:
	psql --file=db/branches.sql ibolc ibolc

reset:
	psql --file=db/reset.sql ibolc ibolc
