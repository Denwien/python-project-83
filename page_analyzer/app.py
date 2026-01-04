import os
from datetime import datetime
from urllib.parse import urlparse

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from validators import url as validate_url
from psycopg2.extras import RealDictCursor

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
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            '''
            SELECT u.*,
                   MAX(c.created_at) AS last_check,
                   MAX(c.status_code) AS status_code
            FROM urls u
            LEFT JOIN url_checks c ON u.id = c.url_id
            GROUP BY u.id
            ORDER BY u.id DESC
            '''
        )
        urls = cur.fetchall()
    return render_template('urls.html', urls=urls)


@app.get('/urls/<int:id>')
def url_show(id):
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute('SELECT * FROM urls WHERE id = %s', (id,))
        url = cur.fetchone()

        cur.execute(
            '''
            SELECT id, status_code, h1, title, description, created_at
            FROM url_checks
            WHERE url_id = %s
            ORDER BY created_at DESC
            ''',
            (id,)
        )
        url_checks = cur.fetchall()

    return render_template('url.html', url=url, url_checks=url_checks)


@app.post('/urls/<int:url_id>/checks')
def create_check(url_id):
    conn = get_connection()

    try:
        # Получаем URL
        with conn.cursor() as cur:
            cur.execute('SELECT name FROM urls WHERE id = %s', (url_id,))
            url = cur.fetchone()[0]

        # Запрос к сайту
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        # SEO-анализ через BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        h1_tag = soup.find('h1')
        title_tag = soup.find('title')
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})

        h1 = h1_tag.get_text(strip=True) if h1_tag else None
        title = title_tag.get_text(strip=True) if title_tag else None
        description = (
            meta_desc_tag['content'].strip()
            if meta_desc_tag and meta_desc_tag.get('content')
            else None
        )

        # Сохраняем проверку
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    '''
                    INSERT INTO url_checks (
                        url_id,
                        status_code,
                        h1,
                        title,
                        description,
                        created_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ''',
                    (
                        url_id,
                        response.status_code,
                        h1,
                        title,
                        description,
                        datetime.now()
                    )
                )

        flash('Страница успешно проверена', 'success')

    except RequestException:
        flash('Произошла ошибка при проверке', 'danger')

    finally:
        conn.close()

    return redirect(url_for('url_show', id=url_id))


if __name__ == '__main__':
    app.run(debug=True)
