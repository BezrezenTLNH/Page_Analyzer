import os
from flask import (Flask, render_template, request, flash, get_flashed_messages, redirect, url_for)
from dotenv import load_dotenv
import page_analyzer.db_commands as db


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def root_get():
    return render_template('main.html')


@app.route('/urls')
def urls():
    urls = db.get_all_data()
    return render_template('urls.html', urls=urls)


@app.route('/urls', methods=['POST'])
def create_urls():
    url = request.form.get('url')

    if not url:
        flash('URL обязателен', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('main.html', messages=messages), 422

    if not db.url_valide(url):
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('main.html', messages=messages), 422

    url = db.url_normalize(url)

    if db.get_id(url):
        id = db.get_id(url)
        flash('Страница уже существует', 'alert-info')
        return redirect(url_for('url_get', id=id))

    id = db.add_data(url)

    if id is None:
        flash('Something wrong', 'alert-danger')
        msgs = get_flashed_messages(with_categories=True)
        return render_template('index.html', url=url, msgs=msgs), 422

    flash('Страница успешно добавлена', 'alert-success')
    return redirect(url_for('get_site', id=id), code=302)


@app.route('/urls/<int:id>', methods=['GET'])
def get_url(id):
    url = db.get_url_data(id)
    msgs = get_flashed_messages(with_categories=True)
    return render_template('url_get.html', url=url, msgs=msgs)