from contextlib import asynccontextmanager
from app.core.db import pool, init_db

@asynccontextmanager
async def lifespan(app):
    # 起動時
    pool.open()
    try:
        init_db()   # ここでテーブル作成（不要なら削除）
    except Exception:
        # 起動失敗を早期に気づける
        pool.close()
        raise

    yield

    # 終了時
    pool.close()