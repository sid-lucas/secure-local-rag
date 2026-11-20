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

## V1

### Setup

- Documents: personal files (transcripts, project reports, CV, letters), mostly PDF
- Index: 175 pages, 335 chunks
- Settings: `CHUNK_SIZE = 512`, `CHUNK_OVERLAP = 50`, `TOP_K = 3`

### Test results

| Test | Result |
|---|---|
| Precise fact | OK |
| Question in English on French documents | OK |
| Missing information | OK |
| Value in a table | Partial: works with the full course name, not with its acronym |
| Short fact in a long document | Partial: found only when the document is named in the question |
| Information spread over several documents | Partial: incomplete answer presented as complete |
| Ambiguous question ("what is the person's address?") | KO: returns an example e-mail address repeated in a report |


### Known issues

**Search**
- Short facts and acronyms are often missed, especially in long documents.
- Only 3 passages are used per answer, so information spread over many documents is incomplete.
- Several passages from the same document can be returned, leaving less room for others.

**Document reading**
- Tables and cover pages in PDFs are not always read correctly.

**Answers**
- The model sometimes adds its own interpretation instead of sticking to the documents.
- Ambiguous questions are answered with the closest content (e.g. an example e-mail address from a report) instead of asking for clarification.

**Security and data**
- A deleted file stays searchable until the index is rebuilt with `--reset`.
- The index is an unencrypted copy of the documents: using a cloud model would send passages to the provider.
- Anything written in the documents can come out in an answer, including example data or sensitive data.