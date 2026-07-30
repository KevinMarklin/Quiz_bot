FROM python:3.11-slim

# Отключаем буферизацию вывода Python и запись .pyc файлов
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Устанавливаем системные зависимости (для сборки некоторых пакетов, если нужно)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . .

# Команда запуска: сперва накатываем миграции Alembic, затем запускаем бота
CMD ["sh", "-c", "alembic upgrade head && python main.py"]