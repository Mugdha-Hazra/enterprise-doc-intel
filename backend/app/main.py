# ==========================================
# Enterprise Document Intelligence System
# Backend Application Entry Point
# ==========================================

from fastapi import FastAPI
import logging

from app.routes import root, health, upload, search

# -------------------------------
# Logging Configuration
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------------------
# FastAPI App Setup
# -------------------------------
app = FastAPI(
    title="Enterprise Document Intelligence System",
    version="0.1.0"
)

# -------------------------------
# Register Routers
# -------------------------------
app.include_router(root.router)
app.include_router(health.router)
app.include_router(upload.router)
app.include_router(search.router)

# -------------------------------
# Application Lifecycle Events
# -------------------------------
@app.on_event("startup")
async def on_startup():
    logger.info("Enterprise Document Intelligence API started successfully")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Enterprise Document Intelligence API shut down")
