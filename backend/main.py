from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.rag.pipeline import create_rag_prompt
from backend.rag.llm_local_small import generate_answer


app = FastAPI(
    title="DocuMed RAG API",
    description="Medical document question answering system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():

    return {
        "message": "DocuMed RAG API is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:

        return {
            "error": "Question cannot be empty"
        }


    # Retrieve relevant documents
    result = create_rag_prompt(question)


    # Generate answer
    answer = generate_answer(
        result["prompt"]
    )


    # Prepare source information
    sources = []

    for metadata, distance in zip(
        result["metadata"],
        result["distances"]
    ):

        sources.append({
            "source": metadata["source"],
            "page": metadata["page"],
            "distance": round(float(distance), 4)
        })


    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }