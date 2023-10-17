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
                cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT id FROM urls WHERE name=%s", (url,))
            id = cursor.fetchone()['id']

            return id if id else None


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
