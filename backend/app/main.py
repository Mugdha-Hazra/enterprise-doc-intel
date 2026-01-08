# ==========================================
# Enterprise Document Intelligence System
# Backend Application Entry Point
# ==========================================
# Responsibilities of this file:
# 1. Create FastAPI application instance
# 2. Configure logging
# 3. Register API routers
# 4. Handle application startup/shutdown
#
# NO business logic lives here
# ==========================================

from fastapi import FastAPI # FastAPI framework for building APIs
import logging  # Standard logging module

from app.routes import root, health, upload # Importing route modules

# -------------------------------
# Logging Configuration
# -------------------------------
logging.basicConfig( # Configure logging settings
    level=logging.INFO, # Set logging level to INFO
    # Eg: DEBUG, INFO, WARNING, ERROR, CRITICAL
    # Eg: INFO level logs general operational information such as startup/shutdown events
    format="%(asctime)s [%(levelname)s] %(message)s" # Define log message format
    # Eg: timestamp, log level, message
    # such as "2023-10-01 12:00:00 [INFO] Application started"
)
logger = logging.getLogger(__name__) # Create a logger instance for this module

# -------------------------------
# FastAPI App Setup
# -------------------------------
app = FastAPI( # Create FastAPI application instance for the backend service such as document processing and extraction
    title="Enterprise Document Intelligence System", # Application title
    version="0.1.0" # Application version
)

# -------------------------------
# Register Routers
# -------------------------------

app.include_router(root.router) # Include the root router such as health check and upload endpoints
app.include_router(health.router) # Include the health check router such as system status endpoints
app.include_router(upload.router) # Include the upload router such as document upload and processing endpoints
# router is getting from route.py, health.py, upload.py respectively for modular route management
# -------------------------------
# Application Lifecycle Events
# -------------------------------
@app.on_event("startup") # Define startup event handler
async def on_startup(): # Startup event function
    logger.info("Enterprise Document Intelligence API started successfully") # Log startup message

@app.on_event("shutdown") # Define shutdown event handler
async def on_shutdown(): # Shutdown event function
    logger.info("Enterprise Document Intelligence API shut down") # Log shutdown message