import os

from page_analyzer.db_commands import (add_data, get_url_data,
                                       check_url, get_check_url,
                                       make_connection)
from page_analyzer.utils import url_parse
import pytest
from dotenv import load_dotenv
import page_analyzer


load_dotenv()
URL = 'http://localhost:8000'
DATABASE_URL = os.getenv('DATABASE_URL')
TESTING_URL = 'https://docs.djangoproject.com'


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
    conn = make_connection()
    id = add_data(TESTING_URL, conn)
    assert get_url_data(id, conn)['name'] == 'https://docs.djangoproject.com'


def test_check_url():
    conn = make_connection()
    id = add_data(TESTING_URL, conn)
    page_data = url_parse(TESTING_URL)
    check_url(id, page_data, conn)
    result = get_check_url(id, conn)[0]
    assert result['id'] == 1
    assert result['status_code'] == 200
    assert result['title'] == \
           "Django documentation | Django documentation | Django"
