from fastapi import FastAPI

app = FastAPI(title="Enterprise Document Intelligence System")

@app.get("/health")
def health_check():
    return {"status": "ok"}
