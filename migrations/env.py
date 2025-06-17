from logging.config import fileConfig
import toml
from sqlalchemy import engine_from_config, pool
from alembic import context

from core.database.models.user import Info_user  # noqa
from core.database.models.base import Base

# === Загружаем DSN из config.toml ===
configs = toml.load("config.toml")
dsn = configs["database"]["dsn"]

# === Приводим DSN к синхронному виду ===
if dsn.startswith("postgres://"):
    dsn = dsn.replace("postgres://", "postgresql+psycopg2://", 1)
elif dsn.startswith("postgresql://"):
    dsn = dsn.replace("postgresql://", "postgresql+psycopg2://", 1)
elif "asyncpg" in dsn:
    dsn = dsn.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)

# === Alembic Config ===
config = context.config

# Настройка логгирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Передаём DSN в alembic.ini
config.set_main_option("sqlalchemy.url", dsn)

# Метаданные моделей
target_metadata = Base.metadata

# === OFFLINE MODE ===
def run_migrations_offline() -> None:
    context.configure(
        url=dsn,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# === ONLINE MODE ===
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

# Вызываем нужный режим
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()