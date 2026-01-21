import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from requests.exceptions import RequestException
from validators import url as validate_url

from page_analyzer.db import (
    add_url,
    add_url_check,
    get_all_urls,
    get_url_by_id,
    get_url_checks_by_url_id,
    get_url_name_by_id,
)
from page_analyzer.parser import parse_html
from page_analyzer.url_normalizer import normalize_url

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def urls_create():
    url = request.form.get('url')

    if not url or not validate_url(url) or len(url) > 255:
        flash('Некорректный URL', 'danger')
        return render_template('index.html'), 422

    normalized_url = normalize_url(url)
    url_id, is_new = add_url(normalized_url, datetime.now())

    if is_new:
        flash('Страница успешно добавлена', 'success')
    else:
        flash('Страница уже существует', 'info')

    return redirect(url_for('url_show', id=url_id))


@app.get('/urls')
def urls_index():
    urls = get_all_urls()
    return render_template('urls.html', urls=urls)


@app.get('/urls/<int:id>')
def url_show(id):
    url = get_url_by_id(id)
    url_checks = get_url_checks_by_url_id(id)
    return render_template('url.html', url=url, url_checks=url_checks)


@app.post('/urls/<int:url_id>/checks')
def create_check(url_id):
    try:
        # Получаем URL
        url = get_url_name_by_id(url_id)
        if not url:
            flash('URL не найден', 'danger')
            return redirect(url_for('urls_index'))

        # Запрос к сайту
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        # Парсим HTML
        data = parse_html(response.text)
        h1 = data["h1"]
        title = data["title"]
        description = data["description"]

        # Сохраняем проверку
        add_url_check(
            url_id,
            response.status_code,
            h1,
            title,
            description,
            datetime.now()
        )

        flash('Страница успешно проверена', 'success')

    except RequestException:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('url_show', id=url_id))


if __name__ == '__main__':
    app.run(debug=True)
