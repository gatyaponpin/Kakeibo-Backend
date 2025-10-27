import os
from psycopg_pool import ConnectionPool

def build_conn_url():
    # DATABASE_URL があればそれを優先
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    # 分割形式から組み立てる
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([host, name, user, password]):
        raise RuntimeError("DB 接続情報が不足しています")

    return f"postgresql://{user}:{password}@{host}:{port}/{name}?sslmode=require"

DATABASE_URL = build_conn_url()

pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=2, timeout=10.0)

def get_conn():
    return pool.connection()
