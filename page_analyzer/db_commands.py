import os
import psycopg2
import psycopg2.extras
from datetime import date
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


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


def check_url(id, status_code, h1, title, description):
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
