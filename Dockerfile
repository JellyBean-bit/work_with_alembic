FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей включая netcat
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Установка uv
RUN pip install uv

# Копирование файла зависимостей
COPY pyproject.toml ./

# Установка зависимостей через uv
RUN uv pip install --system -r pyproject.toml

# Копирование исходного кода
COPY . .

# Создание entrypoint скрипта
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]