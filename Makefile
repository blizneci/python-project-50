opts?=--help

install:
	poetry install

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

lint:
	poetry run flake8 .

selfcheck:
	poetry check

check: selfcheck test lint

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-reinstall:
	python3 -m pip install --user --force-reinstall dist/*.whl

package-uninstall:
	python3 -m pip uninstall hexlet-code

gendiff:
	poetry run gendiff $(opts)

.PHONY: gendiff install test lint selfcheck check build publish package-install
