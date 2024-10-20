MODULES = firsttuto/*.py firsttuto/*/*.py
MODULES_TESTED = firsttuto/*.py firsttuto/*/*.py


.PHONY: typehint
typehint:
	mypy --ignore-missing-imports ${MODULES_TESTED}

.PHONY: lint
lint:
	pylint ${MODULES}

.PHONY: format
format:
	yapf -ir ${MODULES}


.PHONY: clean
clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
	find . -type d -name .mypy_cache | xargs rm -fr
	find . -type f -name .coverage | xargs rm -fr
	find . -type f -name .flaskenv | xargs rm -fr
	find . -type d -name .idea/ | xargs rm -fr

.PHONY: verif
verif: clean typehint lint coverage format clean


.PHONY: loaddata
loaddata:
	python3 manage.py loaddata db.json

.PHONY: run
run:
	python3 manage.py runserver

.PHONY : tests
tests:
	./manage.py test firsttuto.LesProduits.tests

