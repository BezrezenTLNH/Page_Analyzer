PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

dev:
	poetry run flask --app page_analyzer:app run

install:
	poetry install

lint:
	poetry run flake8 page_analyzer

build:
	./build.sh

selfcheck:
	poetry check

test:
	poetry run pytest

lint:
	poetry run flake8 page_analyzer

check: selfcheck test lint

test-coverage:
	poetry run pytest --cov=page_analyzer tests/ --cov-report xml tests