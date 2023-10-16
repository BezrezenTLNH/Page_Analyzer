import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse
from validators import url as valid


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def url_normalize(url):
    url = url = urlparse(url)
    return f'{url.scheme}://{url.netloc}'

def url_validate(url):
    if len(url) < 255 and valid(url):
        return True


def get_id(url):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM urls WHERE name=%s", (url,))
        id = cursor.fetchone()
        connection.close()

    return id if id else None


def add_data(url):
    if get_id(url):
        return None
    else:
        try:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute('INSERT INTO urls (name, created_at)'
                                'VALUES (%s, %s) RETURNING id',
                                (url, datetime.now())
                                )
                    conn.commit()

                    id = cur.fetchone()

                    return id

        except psycopg2.Error:
            return None

        finally:
            conn.close()


def get_all_data():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM urls"
            )
            rows = cur.fetchone()

    urls = ({'id': row.id,
             'name': row.name,
             'created_at': row.created_at} for row in rows)

    return urls




def get_url_data(id):
        conn = psycopg2.connect(DATABASE_URL)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM urls WHERE id=%s",
                (id)
            )
            row = cur.fetchone()

        return {'id': row.id,
                'name': row.name,
                'created_at': row.created_at
                }
