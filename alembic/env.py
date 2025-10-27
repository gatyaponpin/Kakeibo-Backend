import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Alembic Config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# DATABASE_URL は Render / ローカルともに利用中のものを流用
db_url = os.getenv("DATABASE_URL")
if not db_url:
    # 分割管理している場合は組み立て
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    pwd  = os.getenv("DB_PASSWORD")
    if all([host, name, user, pwd]):
        db_url = f"postgresql://{user}:{pwd}@{host}:{port}/{name}"
if not db_url:
    raise RuntimeError("DATABASE_URL (または DB_* 変数) が未設定です。")

config.set_main_option("sqlalchemy.url", db_url)

# ▼ モデル未使用のため target_metadata は None のままでOK
target_metadata = None

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
