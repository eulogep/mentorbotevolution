"""
FastAPI gateway mounting the existing Flask app under /api/app for static SPA serving
- Backend still exposes /api/* endpoints via Flask blueprints
- Health check remains at /api/health (FastAPI)
"""
import os
import sys
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.wsgi import WSGIMiddleware

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from main import app as flask_app  # noqa: E402

app = FastAPI(title="Euloge Learning Platform API Gateway", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "fastapi-gateway", "version": "2.0.0"}

# Mount Flask app under /api/app so SPA is accessible at /api/app/
app.mount("/api/app", WSGIMiddleware(flask_app))