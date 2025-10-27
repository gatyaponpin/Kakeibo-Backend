from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.core.db import get_conn

router = APIRouter(tags=["system"])

@router.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@router.get("/health")
def health():
    # アプリのヘルスのみ（本番はこれが推奨）
    return {"ok": True}

@router.get("/health/db")
def health_db():
    # DB接続チェック（開発用）
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1")
            cur.fetchone()
        return {"db": "ok"}
    except Exception as e:
        return {"db": "ng", "error": str(e), "type": type(e).__name__}