#!/bin/bash
set -e

# Проверка переменной окружения DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
  echo "Ошибка: DATABASE_URL не установлена"
  exit 1
fi

echo "Синхронизация зависимостей..."
uv sync

echo "Компиляция Python пакетов..."
python -m compileall .

echo "Подключение к PostgreSQL и инициализация базы..."
# Если есть SQL-скрипт для инициализации
if [ -f init.sql ]; then
  echo "Выполняем init.sql на базе $DATABASE_URL"
  psql "$DATABASE_URL" -f init.sql
fi

echo "База готова, сборка завершена!"
