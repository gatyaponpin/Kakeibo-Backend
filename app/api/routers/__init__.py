from fastapi import FastAPI
from .health import router as health_router
from .categories import router as categories_router
from .kakeibo import router as kakeibo_router

def include_all_routers(app: FastAPI):
    app.include_router(health_router)
    app.include_router(categories_router)
    app.include_router(kakeibo_router)