from fastapi import FastAPI

app = FastAPI(
    title="DocuMed RAG API",
    description="Document-grounded medical information assistant",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "DocuMed RAG API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }