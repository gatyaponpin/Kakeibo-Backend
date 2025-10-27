import os
from pathlib import Path
from dotenv import load_dotenv

# app/.env を優先、無ければルート .env
HERE = Path(__file__).resolve().parents[1]
load_dotenv(HERE / ".env")
load_dotenv()

class Settings:
    # 単一URL or 分割 定義に両対応
    DATABASE_URL = os.getenv("DATABASE_URL")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_SSLMODE = os.getenv("DB_SSLMODE", "require")

    # CORS
    ALLOW_ORIGINS = [
        os.getenv("CORS_ORIGIN_WEB", ""),
        "http://localhost:5173",
        os.getenv("CORS_ORIGIN_APP", ""),
    ]
    # 空文字は除く
    ALLOW_ORIGINS = [o for o in ALLOW_ORIGINS if o]

settings = Settings()