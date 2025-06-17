import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from core.database.models.user import Info_user  # noqa
from core.database.models.base import Base


import toml
configs = toml.load("config.toml")
dsn = configs["database"]["dsn"]


# === Чтение переменной окружения DATABASE_URL ===
# dsn = os.getenv("DATABASE_URL")
# if not dsn:
#     raise RuntimeError("DATABASE_URL не установлена в переменных окружения!")

# === Приведение к синхронному виду (для Alembic) ===
if dsn.startswith("postgres://"):
    dsn = dsn.replace("postgres://", "postgresql+psycopg2://", 1)
elif dsn.startswith("postgresql://"):
    dsn = dsn.replace("postgresql://", "postgresql+psycopg2://", 1)
elif "asyncpg" in dsn:
    dsn = dsn.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)

# === Alembic config ===
config = context.config

# Настройка логов
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Установка DSN в конфигурацию Alembic
config.set_main_option("sqlalchemy.url", dsn)

# Метаданные
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