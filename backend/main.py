import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Ensure backend directory is in sys.path whether executed from repo root or backend dir
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from config import CORS_ORIGINS, HOST, PORT
from api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="WildSense API",
    description="Offline-first AI Nature Exploration Companion API",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for local and LAN phone interaction (matches localhost and private Wi-Fi IPs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+)(?::\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {
        "app": "WildSense",
        "tagline": "Look closer. Then look away.",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    from api.routes import health_check
    return await health_check()

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
