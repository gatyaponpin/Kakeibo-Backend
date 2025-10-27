from fastapi import FastAPI
from .db import get_conn

app = FastAPI()

@app.get("/health")
def health():
    # DBに軽く当ててヘルスチェック（必要なら）
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            cur.fetchone()
    return {"ok": True}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}