from fastapi import FastAPI

app = FastAPI(
    title="IRON GUARD AI",
    description="AI Powered Industrial Safety Operating System",
    version="1.0.0",
)

@app.get("/")
def root():
    return {
        "project": "IRON GUARD AI",
        "status": "Backend Running",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }