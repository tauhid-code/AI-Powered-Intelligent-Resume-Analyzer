"""
FastAPI Backend Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.auth import router as auth_router
from backend.database import init_db

app = FastAPI(
    title="Hirelytics AI API",
    description="Authentication & ATS scoring backend",
    version="1.0.0", 
)

from fastapi.responses import RedirectResponse

@app.get("/", include_in_schema=False)
def redirect_to_frontend():
    return RedirectResponse(url="http://localhost:8501")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup() -> None:
    init_db()


app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "service": "Hirelytics AI"}
