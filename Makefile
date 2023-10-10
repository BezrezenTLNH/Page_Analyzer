install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

lint:
	pip install flake8
	poetry run flake8 page_analyzer:app

test:
	poetry run pytest

coverage:
	poetry add pytest-cov

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

coverage-missing:
	poetry run pytest --cov-report term-missing --cov=app

package-install:
	python3 -m pip install --user dist/*.whl

package-reinstall:
	python3 -m pip install --force-reinstall --user dist/hexlet_code-0.1.0-py3-none-any.whl

build:
	poetry build

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

.PHONY: install test lint selfcheck check build