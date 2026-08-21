from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import shutil

from backend.graph_rag import graph_retriever
from backend.rag.pipeline import create_rag_prompt
from backend.rag.llm_local_small import generate_answer

from backend.rag.pdf_processor import extract_pdf_chunks
from backend.rag.embeddings import embed_texts
from backend.rag.vectorstore import add_documents


from backend.graph_rag.graph_builder import build_graph
from backend.graph_rag.graph_pipeline import graph_answer


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

class GraphQuestionRequest(BaseModel):
    question: str

# ========================================
# ROOT
# ========================================

@app.get("/")
def root():

    return {
        "message": "DocuMed RAG API is running"
    }


# ========================================
# ASK QUESTION
# ========================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:

        return {
            "error": "Question cannot be empty"
        }

    # Retrieve relevant documents
    result = create_rag_prompt(question)

    # Generate answer using local Qwen
    answer = generate_answer(
        result["prompt"]
    )

    # Prepare source information
    sources = []

    for metadata, distance, document in zip(
        result["metadata"],
        result["distances"],
        result["documents"]
    ):

        similarity = 1 - float(distance)

        sources.append({
            "source": metadata["source"],
            "page": metadata["page"],
            "similarity": round(similarity, 4),
            "chunk": document
        })

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }


@app.post("/graph-ask")
def graph_ask(request: GraphQuestionRequest):

    question = request.question.strip()

    if not question:
        return {
            "error": "Question cannot be empty"
        }

    # Graph RAG logic
    result = graph_retriever(question)

    return {
        "question": question,
        "answer": result["answer"],
        "sources": result.get("sources", [])
    }

@app.get("/graph")
def get_knowledge_graph():

    graph = graph_retriever.get_graph()

    nodes = [
        {
            "id": str(node),
            "label": str(node)
        }
        for node in graph.nodes
    ]

    edges = []

    for edge in graph.edges:

        # If your graph edges contain relationship information
        if isinstance(edge, dict):
            edges.append({
                "source": str(edge.get("source")),
                "target": str(edge.get("target")),
                "label": str(edge.get("relationship", "related"))
            })

        else:
            # For simple edge tuples
            edges.append({
                "source": str(edge[0]),
                "target": str(edge[1]),
                "label": "related"
            })

    return {
        "nodes": nodes,
        "edges": edges
    }

# ========================================
# UPLOAD PDF
# ========================================

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    # Check file type
    if not file.filename.lower().endswith(".pdf"):

        return {
            "success": False,
            "message": "Only PDF files are supported."
        }


    # Create upload directory
    upload_directory = "data/uploads"

    os.makedirs(
        upload_directory,
        exist_ok=True
    )


    # Save PDF
    file_path = os.path.join(
        upload_directory,
        file.filename
    )


    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    # Extract text and create chunks
    chunks = extract_pdf_chunks(
        pdf_path=file_path,
        source_name=file.filename
    )


    if not chunks:

        return {
            "success": False,
            "message": "Could not extract readable text from this PDF."
        }


    # Create embeddings
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embed_texts(texts)


    # Store in Chroma
    number_of_chunks = add_documents(
        chunks,
        embeddings
    )

    # Build knowledge graph
    number_of_relationships = build_graph(
        chunks
    )


    return {
        "success": True,
        "filename": file.filename,
        "pages": len(set(
            chunk["page"]
            for chunk in chunks
        )),
        "chunks": number_of_chunks,
        "message": (
            f"{file.filename} uploaded and added "
            "to the DocuMed knowledge base."
        )
    }