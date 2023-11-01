import os
import requests
from flask import (Flask, render_template,
                   request, flash, get_flashed_messages,
                   redirect, url_for)
from dotenv import load_dotenv
from page_analyzer.url_parse import url_parse
import page_analyzer.db_commands as db
import page_analyzer.url_validation as uv


load_dotenv()
app = Flask(__name__)
DATABASE_URL = os.getenv('DATABASE_URL')
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def root_get():
    return render_template('main.html')


@app.route('/urls')
def urls_get():
    urls = db.get_data()
    return render_template('urls.html', urls=urls)


@app.route('/urls', methods=['POST'])
def urls_post():
    url = request.form.get('url')

    if not url:
        flash('URL обязателен', 'danger')
        msgs = get_flashed_messages(with_categories=True)
        return render_template('main.html', msgs=msgs), 422

    url = uv.url_normalize(url)

    if not uv.url_validate(url):
        flash('Некорректный URL', 'danger')
        msgs = get_flashed_messages(with_categories=True)
        return render_template('main.html', msgs=msgs), 422

    if db.get_id(url):
        id = db.get_id(url)
        flash('Страница уже существует', 'info')
        return redirect(url_for('url_get', id=id))

    db.add_data(url)
    id = db.get_id(url)

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_get', id=id))


@app.route('/urls/<int:id>')
def url_get(id):
    msgs = get_flashed_messages(with_categories=True)
    url = db.get_url_data(id)
    checks = db.get_check_url(id)

    return render_template('url.html',
                           url=url, checks=checks, msgs=msgs)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def run_check(id):
    url = db.get_url_data(id)['name']
    try:
        status_code, title, h1, description = url_parse(url)

    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')

    else:
        db.check_url(id, status_code, title, h1, description)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('url_get', id=id))

    return redirect(url_for('url_get', id=id))
