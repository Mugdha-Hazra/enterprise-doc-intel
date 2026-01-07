from fastapi import APIRouter # Import APIRouter for creating route groups

router = APIRouter() # Initialize APIRouter instance

@router.get("/health") # Define health check endpoint
def health_check(): # Health check function
    return { # Return healthy status
        "status": "healthy", # Indicate the service is healthy
        "service": "enterprise-doc-intel" # Name of the service
    }
