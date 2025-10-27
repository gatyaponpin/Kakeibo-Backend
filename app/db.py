import os
from psycopg_pool import ConnectionPool

# Render Postgres の接続文字列（例：postgres://..../dbname?sslmode=require）
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

# プールを1つだけ作る（アプリ起動時）
pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=5)

def get_conn():
    # with get_conn() as conn: で使えるように
    return pool.connection()