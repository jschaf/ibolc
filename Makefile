.phony: install
install:
	pgxn install ssn
	pgxn load -d ibolc ssn

.PHONY: createdb
createdb:
	createuser ibolc
	createdb ibolc --encoding=utf8 --owner=ibolc

.PHONY: connect
connect:
	psql ibolc ibolc

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

