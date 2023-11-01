import os

import page_analyzer.db_commands as pa
import pytest
from dotenv import load_dotenv
import page_analyzer


load_dotenv()
URL = 'http://localhost:8000'
DATABASE_URL = os.getenv('DATABASE_URL')
TESTING_URL = 'https://career.habr.com'


@pytest.fixture()
def app():
    app = page_analyzer.app
    app.config.update({
        "ENV": 'testing',
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_get_root(client):
    response = client.get('/')
    assert response.status_code == 200


def test_add_data():
    pa.add_data(TESTING_URL)
    id = pa.get_id(TESTING_URL)
    assert pa.get_url_data(id)['name'] == 'https://career.habr.com'


def test_check_url():
    pa.add_data(TESTING_URL)
    id = pa.get_id(TESTING_URL)
    status_code, h1, title, description = pa.parser(TESTING_URL)
    pa.check_url(id, status_code, h1, title, description)
    assert pa.get_check_url(id)[0]['id'] == 1
    assert pa.get_check_url(id)[0]['status_code'] == 200
    assert pa.get_check_url(id)[0]['title'] == \
           'Работа в IT-индустрии, свежие вакансии и резюме,' \
           ' поиск работы — Хабр Карьера'
