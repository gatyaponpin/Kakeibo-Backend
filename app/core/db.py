from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from psycopg_pool import ConnectionPool
from app.core.settings import settings

def _build_url_from_parts():
    if not all([settings.DB_HOST, settings.DB_NAME, settings.DB_USER, settings.DB_PASSWORD]):
        return None
    return f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@" \
           f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

def _augment_conninfo(url: str) -> str:
    parsed = urlparse(url)
    q = dict(parse_qsl(parsed.query))
    q.setdefault("sslmode", settings.DB_SSLMODE)
    q.setdefault("connect_timeout", "5")
    q.setdefault("keepalives", "1")
    q.setdefault("keepalives_idle", "30")
    q.setdefault("keepalives_interval", "10")
    q.setdefault("keepalives_count", "5")
    return urlunparse(parsed._replace(query=urlencode(q)))

_raw = settings.DATABASE_URL or _build_url_from_parts()
if not _raw:
    raise RuntimeError("DB接続情報が不足しています。DATABASE_URL または DB_HOST/USER/PASSWORD を設定してください。")

CONNINFO = _augment_conninfo(_raw)

pool = ConnectionPool(
    conninfo=CONNINFO,
    min_size=1,
    max_size=2,
    timeout=10.0,
)

def get_conn():
    return pool.connection()

def init_db():
    ddl = """
    CREATE TABLE IF NOT EXISTS todos (
        id BIGSERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT FALSE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(ddl)
        conn.commit()
