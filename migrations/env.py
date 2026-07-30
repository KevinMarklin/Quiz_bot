import os
import sys
from dotenv import load_dotenv

from sqlalchemy import engine_from_config, pool
from alembic import context

# 1. Загружаем переменные из .env файла
load_dotenv()

# 2. Добавляем корень проекта в sys.path (чтобы импорты core... работали корректно)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 3. Импортируем базовый класс и ВСЕ модели, чтобы Alembic их увидел
from core.database.models.base import Base
from core.database.models.user import Info_user  # noqa: F401

# Если есть другие файлы с моделями (например, quiz.py, stats.py и т.д.), 
# их ТОЖЕ нужно импортировать здесь, чтобы таблицы попали в autogenerate:
# from core.database.models.quiz import Quiz  # noqa: F401

# 4. Чтение переменной окружения DATABASE_URL
dsn = os.getenv("DATABASE_URL")
if not dsn:
    raise RuntimeError("DATABASE_URL не установлена в переменных окружения!")

# 5. Приведение к синхронному драйверу для Alembic
if dsn.startswith("postgres://"):
    dsn = dsn.replace("postgres://", "postgresql+psycopg2://", 1)
elif dsn.startswith("postgresql://"):
    dsn = dsn.replace("postgresql://", "postgresql+psycopg2://", 1)
elif "asyncpg" in dsn:
    dsn = dsn.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)

# Передаем итоговый dsn в конфигурацию Alembic
config = context.config
config.set_main_option("sqlalchemy.url", dsn)

# Связываем метаданные SQLAlchemy для автогенерации
target_metadata = Base.metadata

# === OFFLINE mode ===
def run_migrations_offline() -> None:
    context.configure(
        url=dsn,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# === ONLINE mode ===
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

# === Запуск ===
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()