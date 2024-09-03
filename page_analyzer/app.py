from flask import (Flask, render_template, request,
                   flash, url_for, redirect, make_response)
from dotenv import load_dotenv
from page_analyzer.validator import validate, normalize_url
from page_analizer.db import (get_urls_data, get_id_by_url_name,
                              add_url, get_url_by_id, get_checks_by_url_id)
import os


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def urls_get():
    urls = get_urls_data()
    return render_template(
        'urls.html',
        urls=urls,
    )


@app.post('/urls')
def add_url():
    get_url = request.form['url']
    norm_url = normalize_url(get_url)
    error = validate(norm_url)
    if error:
        flash(error, 'alert alert-danger')
        return render_template(
            'index.html',
            url=get_url
        ), 422
    url_id = get_id_by_url_name(norm_url)
    if url_id:
        flash('Страница уже существует', 'alert alert-info')
        return redirect(url_for('get_url', id=url_id), code=302)
    url_id = add_url(url)
    flash('Страница успешно добавлена', 'alert alert-success')
    return make_response(redirect(url_for('get_url', id=url_id), code=302))


@app.route('/urls/<id>')
def get_url(id):
    url = get_url_by_id(id) or {}
    checks = get_checks_by_url_id(id) or []
    return render_template(
        'show.html',
        url=url,
        checks=checks
    )
