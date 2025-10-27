from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .db import get_conn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="My FastAPI on Render")

ALLOWED_ORIGINS = [
    "https://watababekakeibo.netlify.app",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

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