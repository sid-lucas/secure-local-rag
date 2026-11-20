# secure-local-rag

A fully local RAG (Retrieval-Augmented Generation) pipeline over personal documents, built to study how RAG systems fail and how they can be attacked and secured.

Everything runs on the local machine: no document, chunk or question is sent to an external service.

## Stack

- **Framework:** LlamaIndex
- **LLM:** `qwen2.5-coder:14b` via Ollama
- **Embedding model:** `bge-m3` via Ollama (multilingual)
- **Vector store:** Chroma

## Pipeline

```
documents → load → split into chunks → embed → store in Chroma    (ingest.py)
question  → embed → retrieve top-k chunks → LLM writes answer     (query.py)
```

## Project structure

```
├── config.py        # models, paths, chunking and retrieval settings
├── ingest.py        # load, split, embed and store documents
├── query.py         # ask a question, print answer and sources
├── sample_data/     # fictional documents for testing
├── data/            # personal documents (gitignored)
└── chroma_db/       # vector index (gitignored)
```

## Setup

```bash
ollama pull qwen2.5-coder:14b
ollama pull bge-m3

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## Usage

```bash
# Index the fictional sample documents
python ingest.py --source sample_data --reset

# Index personal documents in data/ (default)
python ingest.py --reset

# Ask a question
python query.py "What was the subject of the bachelor thesis?"
```

`--reset` rebuilds the index from scratch. Without it, re-running ingestion duplicates chunks.