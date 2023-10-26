import os
from flask import (Flask, render_template,
                   request, flash, get_flashed_messages,
                   redirect, url_for)
from dotenv import load_dotenv
import page_analyzer.db_commands as db


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

    url = db.url_normalize(url)

    if not db.url_validate(url):
        flash('Некорректный URL', 'danger')
        msgs = get_flashed_messages(with_categories=True)
        return render_template('main.html', msgs=msgs), 422

    if db.get_id(url):
        id = db.get_id(url)
        flash('Страница уже существует', 'info')
        return redirect(url_for('url_get', id=id), code=302)

    db.add_data(url)
    id = db.get_id(url)

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_get', id=id), code=302)


@app.route('/urls/<int:id>')
def url_get(id):
    msgs = get_flashed_messages(with_categories=True)
    url = db.get_url_data(id)
    checks = db.get_check_url(id)

    return render_template('url.html',
                           url=url, checks=checks, msgs=msgs), 422


@app.route('/urls/<int:id>/checks', methods=['POST'])
def run_check(id):
    checks = db.get_check_url(id)
    if not checks:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url_get', id=id), code=302)

    flash('Страница успешно проверена', 'succes')

    return redirect(url_for('url_get', id=id), code=302)
