import os

from page_analyzer.db_commands import (add_data,
                                       get_id, get_url_data,
                                       check_url, get_check_url)
from page_analyzer.url_parse import url_parse
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
    add_data(TESTING_URL)
    id = get_id(TESTING_URL)
    assert get_url_data(id)['name'] == 'https://career.habr.com'


def test_check_url():
    add_data(TESTING_URL)
    id = get_id(TESTING_URL)
    status_code, h1, title, description = url_parse(TESTING_URL)
    check_url(id, status_code, h1, title, description)
    result = get_check_url(id)[0]
    assert result['id'] == 1
    assert result['status_code'] == 200
    assert result['title'] == \
           'Работа в IT-индустрии, свежие вакансии и резюме,' \
           ' поиск работы — Хабр Карьера'
