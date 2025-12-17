#!/bin/bash
set -e

if [ -z "$DATABASE_URL" ]; then
  echo "Ошибка: DATABASE_URL не установлена"
  exit 1
fi

uv sync
python -m compileall .

python <<'EOF'
import os
import psycopg

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL не установлена")

init_file = "init.sql"
if os.path.exists(init_file):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(open(init_file).read())
        conn.commit()
EOF
