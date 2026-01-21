import os
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def add_url(normalized_url: str, created_at: datetime) -> tuple[int | None, bool]:
    """
    Добавляет URL в базу данных.
    Возвращает (url_id, is_new) где is_new=True если URL был добавлен,
    False если уже существовал.
    """
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
                (normalized_url, created_at)
            )
            row = cur.fetchone()

            if row:
                return (row[0], True)
            else:
                cur.execute(
                    'SELECT id FROM urls WHERE name = %s',
                    (normalized_url,)
                )
                url_id = cur.fetchone()[0]
                return (url_id, False)


def get_all_urls():
    """Возвращает все URL с информацией о последней проверке."""
    conn = get_connection()
    with conn:
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
            return cur.fetchall()


def get_url_by_id(url_id: int):
    """Возвращает URL по его ID."""
    conn = get_connection()
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
            return cur.fetchone()


def get_url_name_by_id(url_id: int) -> str | None:
    """Возвращает имя URL по его ID."""
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute('SELECT name FROM urls WHERE id = %s', (url_id,))
            row = cur.fetchone()
            return row[0] if row else None


def get_url_checks_by_url_id(url_id: int):
    """Возвращает все проверки для указанного URL."""
    conn = get_connection()
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                '''
                SELECT id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id = %s
                ORDER BY created_at DESC
                ''',
                (url_id,)
            )
            return cur.fetchall()


def add_url_check(
    url_id: int,
    status_code: int,
    h1: str | None,
    title: str | None,
    description: str | None,
    created_at: datetime
):
    """Добавляет проверку URL в базу данных."""
    conn = get_connection()
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
                    status_code,
                    h1,
                    title,
                    description,
                    created_at
                )
            )
