PROD_PATH_ROOT := /home/jschaf/webapps/ibolc_app
PROD_PATH := $(PROD_PATH_ROOT)/ibolc

PROD_SSH_USER := jschaf@jschaf.com

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

.PHONY: deploy
deploy: rsync setup-python setup-apache apache-restart

.PHONY: rsync
rsync:
	rsync --delete --archive --verbose --compress          \
	  --exclude .git/ --exclude .gitignore --exclude venv/ \
	  --exclude __pycache                                  \
	  ./                                                   \
	  $(PROD_SSH_USER):$(PROD_PATH)

# TODO: Verify that IBOLC_ENV is set to 'prod'

.PHONY: setup-python
setup-python:
	ssh $(PROD_SSH_USER) "cd $(PROD_PATH)     \
    && ( [ -d venv ] || pyvenv-3.4 venv )   \
	  && source venv/bin/activate		          \
	  && pip install -q -r requirements.txt"

.PHONY: setup-apache
setup-apache:
	ssh $(PROD_SSH_USER) "cd $(PROD_PATH_ROOT) \
    &&  rm -f apache2/conf/httpd.conf        \
    && cp ibolc/scripts/httpd.conf apache2/conf/"

.PHONY: apache-stop
apache-stop:
	ssh $(PROD_SSH_USER) "cd $(PROD_PATH_ROOT) \
    && apache2/bin/stop"

.PHONY: apache-start
apache-start:
	ssh $(PROD_SSH_USER) "cd $(PROD_PATH_ROOT) \
    && apache2/bin/start"


.PHONY: apache-restart
apache-restart:
	ssh $(PROD_SSH_USER) "cd $(PROD_PATH_ROOT) \
    && apache2/bin/restart"
