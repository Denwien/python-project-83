#!/bin/bash
set -e

curl -LsSf https://astral.sh/uv/install.sh | sh
. $HOME/.local/bin/env

if [ -z "$DATABASE_URL" ]; then
  echo "Ошибка: DATABASE_URL не установлена"
  exit 1
fi

make install
psql -a -d "$DATABASE_URL" -f database.sql
