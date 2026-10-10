from contextlib import asynccontextmanager
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

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
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
