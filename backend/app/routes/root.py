from fastapi import APIRouter # use : it is needed for creating route groups

router = APIRouter() # create a router instance

@router.get("/") # define a GET endpoint at the root path
def root(): # define the root endpoint function
    return {
        "service": "Enterprise Document Intelligence API",
        "status": "running",
        "version": "phase-1"
    }
#describe : This code sets up a basic FastAPI router with a single GET endpoint
# at the root path ("/").
# When accessed, this endpoint returns a JSON response indicating the service name,
# its running status, and the version.
# The APIRouter instance allows for organizing routes in a modular way within the application.
