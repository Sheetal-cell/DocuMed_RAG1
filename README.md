# DocuMed RAG

DocuMed is a medical-information Retrieval-Augmented Generation (RAG) application.

It retrieves relevant information from medical PDF documents stored in a local ChromaDB vector database and uses a locally loaded Qwen language model with a DocuMed LoRA adapter to generate answers grounded in the retrieved context.

> **Medical safety:** DocuMed is an information/research assistant, not a doctor or diagnostic system. It must not be used for diagnosis, emergency decisions, or personalized treatment.

---

## 1. Project Architecture

```text
DocuMed_RAG1/
├── backend/
│   ├── main.py
│   ├── ingest.py
│   ├── test_loader.py
│   ├── test_embeddings.py
│   ├── test_retrieval.py
│   ├── test_rag.py
│   └── rag/
│       ├── embeddings.py
│       ├── vectorstore.py
│       ├── prompt.py
│       ├── llm.py
│       └── pipeline.py
├── data/
│   └── heart.pdf
├── models/
│   └── documed-qwen-lora/
├── chroma_db/
├── frontend/
├── .venv/
└── README.md
```

---

## 2. Technologies

### Backend
- Python 3.11
- FastAPI
- Uvicorn
- PyMuPDF
- Sentence Transformers
- ChromaDB
- PyTorch
- Hugging Face Transformers
- PEFT / LoRA

### Frontend
- React
- TypeScript
- Vite
- ESLint
- npm

### ML / RAG
- Qwen language model
- DocuMed LoRA adapter
- `sentence-transformers/all-MiniLM-L6-v2`
- ChromaDB

---

## 3. Requirements

Recommended:

- Windows 10/11
- Python 3.11
- Node.js + npm
- Git
- VS Code
- Internet connection for initial Hugging Face downloads

A GPU is strongly recommended for local LLM inference.

The training workflow used Google Colab GPU. The local application uses the smaller Qwen model so local inference is practical.

---

# 4. Clone / Open the Repository

```powershell
git clone <YOUR_REPOSITORY_URL>
cd DocuMed_RAG1
```

If already cloned:

```powershell
cd C:\Users\sheet\OneDrive\Desktop\All\DocuMed_RAG1
```

---

# 5. Create the Python Environment

From the project root:

```powershell
python -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv)
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again.

---

# 6. Install Backend Dependencies

```powershell
pip install fastapi uvicorn
pip install pymupdf
pip install sentence-transformers
pip install chromadb
pip install torch
pip install transformers
pip install peft
```

If the repository later contains `requirements.txt`, use:

```powershell
pip install -r requirements.txt
```

---

# 7. Check Python and GPU

```powershell
python --version
```

Expected:

```text
Python 3.11.x
```

Check PyTorch:

```powershell
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"
```

GPU name:

```powershell
python -c "import torch; print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

---

# 8. Add Medical Documents

Place source PDFs inside:

```text
data/
```

Example:

```text
data/heart.pdf
```

The PDF is processed into:

```text
PDF
→ pages
→ text chunks
→ embeddings
→ ChromaDB
```

---

# 9. Test PDF Loading

```powershell
python backend/test_loader.py
```

Example successful output:

```text
Number of pages: 42
PAGE: 1
Technical package for cardiovascular disease
management in primary health care
```

---

# 10. Test Embeddings

```powershell
python backend/test_embeddings.py
```

Expected:

```text
Chunks: 57
Embeddings: 57
Embedding dimension: 384
```

The embedding model is:

```text
sentence-transformers/all-MiniLM-L6-v2
```

---

# 11. Build the Vector Database

```powershell
python backend/ingest.py
```

Expected:

```text
Pages loaded: 42
Total chunks: 57
Embeddings created: 57
Documents successfully added to ChromaDB!
```

Run ingestion again when source documents change and the vector database needs updating.

---

# 12. Test Retrieval

```powershell
python backend/test_retrieval.py
```

You should see results such as:

```text
RESULT 1
Source: heart.pdf
Page: 8

RESULT 2
Source: heart.pdf
Page: 9
```

The returned distance is the vector-search distance from ChromaDB.

---

# 13. DocuMed LoRA Adapter

The trained adapter is stored in:

```text
models/documed-qwen-lora/
```

Important files include:

```text
adapter_model.safetensors
adapter_config.json
tokenizer.json
tokenizer_config.json
chat_template.jinja
training_args.bin
```

The LoRA adapter is loaded on top of the Qwen base model.

The adapter is not itself a complete standalone language model.

---

# 14. Test the Complete RAG Pipeline

```powershell
python backend/test_rag.py
```

The pipeline is:

```text
Question
   ↓
Embedding
   ↓
ChromaDB Retrieval
   ↓
Relevant Medical Context
   ↓
Prompt Construction
   ↓
DocuMed Qwen
   ↓
Answer
```

A successful run should show:

```text
RETRIEVED SOURCES
PROMPT SENT TO QWEN
DOCUMED ANSWER
```

---

# 15. Start FastAPI

From the project root:

```powershell
uvicorn backend.main:app --reload
```

Expected:

```text
Uvicorn running on http://127.0.0.1:8000
```

Do **not** type the log line itself as a command.

The command is:

```powershell
uvicorn backend.main:app --reload
```

---

# 16. Test the `/ask` Endpoint

PowerShell:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/ask" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"question":"What is the HEARTS technical package and what is its purpose?"}'
```

A successful response contains:

```text
question
answer
```

---

# 17. Start the React Frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Expected:

```text
Local: http://localhost:5173/
```

Open:

```text
http://localhost:5173/
```

The frontend communicates with the FastAPI backend at:

```text
http://127.0.0.1:8000
```

---

# 18. Run the Full Application

## Terminal 1 — Backend

```powershell
cd C:\Users\sheet\OneDrive\Desktop\All\DocuMed_RAG1
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload
```

## Terminal 2 — Frontend

```powershell
cd C:\Users\sheet\OneDrive\Desktop\All\DocuMed_RAG1\frontend
npm run dev
```

Then open:

```text
http://localhost:5173/
```

---

# 19. Google Colab Training

The DocuMed LoRA adapter was trained using a GPU environment in Google Colab.

Training workflow:

```text
Dataset
  ↓
Qwen tokenizer
  ↓
QLoRA / LoRA preparation
  ↓
SFTTrainer
  ↓
Training
  ↓
DocuMed LoRA adapter
```

The resulting adapter is used locally from:

```text
models/documed-qwen-lora/
```

Training and inference are separate stages. You do not need to retrain the model every time the application starts.

---

# 20. RAG vs Fine-Tuning

### Fine-tuning / LoRA

Teaches the model desired response behavior:

```text
Base Qwen
   ↓
LoRA training
   ↓
DocuMed adapter
```

### RAG

Supplies relevant information at inference time:

```text
Question
   ↓
Embedding
   ↓
ChromaDB
   ↓
Relevant chunks
   ↓
Prompt
   ↓
Qwen
```

In this project:

```text
LoRA = how the model should respond
RAG  = what information the model should use
```

---

# 21. Common Problems

## `ModuleNotFoundError: No module named 'rag'`

Run Uvicorn from the project root:

```powershell
cd C:\Users\sheet\OneDrive\Desktop\All\DocuMed_RAG1
uvicorn backend.main:app --reload
```

Do not run it from inside `backend/rag`.

---

## `CORSMiddleware is not defined`

Ensure `backend/main.py` contains:

```python
from fastapi.middleware.cors import CORSMiddleware
```

before `CORSMiddleware` is used.

---

## Port 8000 already in use

Stop the existing server with:

```text
CTRL+C
```

or use:

```powershell
uvicorn backend.main:app --reload --port 8001
```

If the port changes, update the frontend API URL.

---

## Hugging Face unauthenticated warning

You may see:

```text
Warning: You are sending unauthenticated requests to the HF Hub.
```

This is a warning, not necessarily an error. The model can still download.

---

## Windows symlink warning

You may see a warning saying that the Hugging Face cache cannot use symlinks.

This normally does not prevent the model from working.

---

## Model takes a long time to load

The first download can be large. Once cached locally, later runs should normally reuse the cached files.

---

## RAG answer is not grounded

Debug each stage separately:

```powershell
python backend/test_retrieval.py
python backend/test_rag.py
```

Check:

1. retrieved pages
2. retrieval distances
3. prompt context
4. model loading
5. LoRA adapter loading

---

# 22. Recommended Development Workflow

When adding a new medical PDF:

```text
1. Put PDF in data/
        ↓
2. Test PDF loader
        ↓
3. Test embeddings
        ↓
4. Run ingestion
        ↓
5. Test retrieval
        ↓
6. Test RAG
        ↓
7. Start FastAPI
        ↓
8. Test /ask
        ↓
9. Start React
        ↓
10. Test complete application
```

Commands:

```powershell
python backend/test_loader.py
python backend/test_embeddings.py
python backend/ingest.py
python backend/test_retrieval.py
python backend/test_rag.py
uvicorn backend.main:app --reload
```

Frontend:

```powershell
cd frontend
npm run dev
```

---

# 23. Safety Rules

DocuMed is designed to:

- answer using retrieved document context
- avoid inventing medical facts
- say when information is unavailable
- mention source documents/pages where possible
- avoid diagnosing users
- avoid prescribing medication
- advise immediate professional care for emergencies

It should not be presented as a replacement for a qualified healthcare professional.

---

# 24. Current Project Status

Completed:

- [x] Medical PDF loading
- [x] Text extraction
- [x] Text chunking
- [x] Sentence-transformer embeddings
- [x] ChromaDB vector storage
- [x] Semantic retrieval
- [x] RAG prompt construction
- [x] Qwen local model loading
- [x] DocuMed LoRA adapter loading
- [x] RAG answer generation
- [x] FastAPI `/ask` endpoint
- [x] React + TypeScript + Vite scaffold

Next development:

- [ ] Complete DocuMed chat UI
- [ ] Source/page display
- [ ] Loading and error states
- [ ] Chat history
- [ ] Improved retrieval/ranking
- [ ] Document upload interface
- [ ] More medical documents
- [ ] RAG evaluation
- [ ] Deployment

---

# 25. Quick Start

If everything is already installed:

### Backend

```powershell
cd C:\Users\sheet\OneDrive\Desktop\All\DocuMed_RAG1
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload
```

### Frontend

In a second terminal:

```powershell
cd C:\Users\sheet\OneDrive\Desktop\All\DocuMed_RAG1\frontend
npm run dev
```

Open:

```text
http://localhost:5173/
```

---

# 26. Git Notes

Avoid committing generated environments and caches:

```text
.venv/
__pycache__/
*.pyc
.env
```

Large model files and vector databases should also be considered carefully before committing them to GitHub.

Use an appropriate model/file-storage strategy for deployment.

---

## DocuMed

**A document-grounded medical RAG assistant built with Python, FastAPI, ChromaDB, Qwen, LoRA, and React.**
