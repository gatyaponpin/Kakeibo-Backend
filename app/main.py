from fastapi import FastAPI
from app.core.cors import setup_cors
from app.core.lifespan import lifespan
from app.api.routers import include_all_routers

# ここは“組み立て”だけ
app = FastAPI(title="My FastAPI", lifespan=lifespan)

setup_cors(app)                 # CORSをひとまとめに
include_all_routers(app)