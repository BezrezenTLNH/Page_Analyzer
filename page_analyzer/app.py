import os
from flask import (Flask, render_template)
from dotenv import load_dotenv
import db_commands as db


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def root_get():
    return render_template('index.html')


@app.route('/urls', methods=['GET'])
def check_url():
    urls = db.add_data()
    return render_template('urls.html', urls=urls)


@app.route('/urls', methods=['POST'])
def create_urls():
    pass


@app.route('/urls/<id>', methods=['GET'])
def check_url_id(id):
    pass