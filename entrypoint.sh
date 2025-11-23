#!/bin/bash

# Ожидание доступности базы данных
echo "Waiting for database to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready!"

# Запуск миграций Alembic 
echo "Running database migrations..."
uv run alembic upgrade head

# Запуск приложения
echo "Starting application..."
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload