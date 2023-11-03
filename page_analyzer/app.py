import os
import requests
from flask import (Flask, render_template,
                   request, flash, get_flashed_messages,
                   redirect, url_for)
from dotenv import load_dotenv
import page_analyzer.db as db
from page_analyzer.utils import (url_normalize,
                                 url_parse, url_validate)


load_dotenv()
app = Flask(__name__)
DATABASE_URL = os.getenv('DATABASE_URL')
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def root_get():
    return render_template('main.html')


@app.route('/urls')
def urls_get():
    conn = db.get_connection()
    urls = db.get_all_urls_and_checks(conn)
    db.close_connection(conn)
    return render_template('urls.html', urls=urls)


@app.route('/urls', methods=['POST'])
def urls_post():
    conn = db.get_connection()
    url = request.form.get('url')

    if not url:
        flash('URL обязателен', 'danger')
        msgs = get_flashed_messages(with_categories=True)
        return render_template('main.html', msgs=msgs), 422

    url = url_normalize(url)

    if not url_validate(url):
        flash('Некорректный URL', 'danger')
        msgs = get_flashed_messages(with_categories=True)
        return render_template('main.html', msgs=msgs), 422

    if id := db.get_id(url, conn):
        flash('Страница уже существует', 'info')
        return redirect(url_for('url_get', id=id))

    id = db.add_data(url, conn)
    db.close_connection(conn)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_get', id=id))


@app.route('/urls/<int:id>')
def url_get(id):
    conn = db.get_connection()
    msgs = get_flashed_messages(with_categories=True)
    url = db.get_url_data(id, conn)
    checks = db.get_check_url(id, conn)
    db.close_connection(conn)

    return render_template('url_details.html',
                           url=url, checks=checks, msgs=msgs)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def run_check(id):
    conn = db.get_connection()
    url = db.get_url_data(id, conn)['name']
    try:
        page_data = url_parse(url)

    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')

    else:
        db.check_url(id, page_data, conn)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('url_get', id=id))
    db.close_connection(conn)
    return redirect(url_for('url_get', id=id))
