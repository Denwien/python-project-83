import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from validators import url as validate_url
from urllib.parse import urlparse
from datetime import datetime

from page_analyzer.db import get_connection

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

    parsed = urlparse(url)
    normalized_url = f'{parsed.scheme}://{parsed.netloc}'

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s)
                ON CONFLICT (name) DO NOTHING
                RETURNING id
                ''',
                (normalized_url, datetime.now())
            )
            row = cur.fetchone()

            if row:
                url_id = row[0]
                flash('Страница успешно добавлена', 'success')
            else:
                cur.execute(
                    'SELECT id FROM urls WHERE name = %s',
                    (normalized_url,)
                )
                url_id = cur.fetchone()[0]
                flash('Страница уже существует', 'info')

    return redirect(url_for('url_show', id=url_id))


@app.get('/urls')
def urls_index():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            'SELECT id, name, created_at FROM urls ORDER BY id DESC'
        )
        urls = cur.fetchall()

    return render_template('urls.html', urls=urls)


@app.get('/urls/<int:id>')
def url_show(id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            'SELECT id, name, created_at FROM urls WHERE id = %s',
            (id,)
        )
        url = cur.fetchone()

    return render_template('url.html', url=url)
