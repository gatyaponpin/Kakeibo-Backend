from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )