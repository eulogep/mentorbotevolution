"""
FastAPI wrapper to expose existing Flask app under /api via Kubernetes ingress
- Runs at 0.0.0.0:8001 by supervisor (do not start manually)
- Mounts the Flask app from /app/main.py using WSGIMiddleware
"""
import os
import sys
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.wsgi import WSGIMiddleware

# Ensure we can import the Flask app from /app/main.py
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from main import app as flask_app  # noqa: E402

app = FastAPI(title="Euloge Learning Platform API Gateway", version="2.0.0")

# CORS (align with platform expectations)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check on FastAPI side
@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "fastapi-gateway", "version": "2.0.0"}

# Mount the existing Flask app at root (so it serves /api/* routes)
app.mount("/", WSGIMiddleware(flask_app))