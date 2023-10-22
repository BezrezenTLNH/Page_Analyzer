import os
import psycopg2
import psycopg2.extras
from datetime import date
from dotenv import load_dotenv
from urllib.parse import urlparse
from validators import url as valid


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def url_normalize(url):
    url = urlparse(url)
    return f'{url.scheme}://{url.netloc}'

def url_validate(url):
    if len(url) < 255 and valid(url):
        return True


def get_id(url):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT id FROM urls WHERE name=%s", (url,))
            result = cur.fetchone()
            id = result['id'] if result else None

            return id


def get_url_data(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE id=%s", (id,))

            return cursor.fetchone()


def add_data(url):
    if get_id(url):
        return None

    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('INSERT INTO urls (name, created_at)'
                        'VALUES (%s, %s)',
                        (url, date.today().isoformat())
                        )
            conn.commit()

            id = get_id(url)

            return id


def get_data():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('SELECT * FROM urls ORDER BY id DESC')

            return cur.fetchall()

def check_url(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('INSERT INTO url_checks (url_id, created_at)'
                        'VALUES (%s, %s)',
                        (id, date.today().isoformat())
                        )
            conn.commit()

            return get_check_url(id)

def get_check_url(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT * FROM url_checks WHERE url_id=%s", (id,))

            return cursor.fetchall()

#  Реализуйте обработчик маршрута POST urls/<id>/checks и форму с кнопкой на странице сайта,
#  при отправке которой происходит создание новой проверки.
#  Обратите внимание, что на этом шаге заполняются только базовые поля
#  (url_id и created_at)

#  1) Найти способ создавать записи в sql на основе другого уникального
#  id (связанные таблицы?)

#  2) Использовать псикорг2 для покключения к дб, написать запрос.
#  заполнить колонки

#  3) Проверить работоспособность

#  4) Написать тесты
