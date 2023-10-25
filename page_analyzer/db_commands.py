import os
import psycopg2
import psycopg2.extras
import requests
from bs4 import BeautifulSoup
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
            cur.execute('''SELECT DISTINCT ON (urls.id) urls.id, name,
            url_checks.created_at, url_checks.status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            ORDER BY urls.id DESC, url_checks.id DESC;''')

            return cur.fetchall()


def check_url(id):
    url = get_url_data(id)[1]
    r = requests.get(url)
    status_code = r.status_code
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.select_one('title')
    h1 = soup.select_one('h1')
    description = soup.select_one('meta[name="description"]')
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('INSERT INTO url_checks (url_id, status_code, '
                        'h1, title, description, created_at)'
                        'VALUES (%s, %s, %s, %s, %s, %s)',
                        ((id, status_code,
                          h1.string if h1 else None,
                          title.string if title else None,
                          description['content'] if description else None,
                          date.today().isoformat())))
            conn.commit()


def get_check_url(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT * FROM url_checks WHERE url_id=%s", (id,))

            return cursor.fetchall()
