

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

.PHONY: flake8
flake8:
	flake8 ibolc

.PHONY: pylint
pylint:
	pylint --rcfile=.pylintrc ibolc

.PHONY: pip-upgrade-all
# See http://stackoverflow.com/questions/2720014/
pip-upgrade-all:
	pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

