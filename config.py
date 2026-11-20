from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "personal_docs"

# Local models (Ollama)
OLLAMA_URL = "http://localhost:11434"
LLM_MODEL = "qwen2.5-coder:14b"
EMBED_MODEL = "bge-m3"  # multilingual
REQUEST_TIMEOUT = 300

# Chunking
CHUNK_SIZE = 512        # tokens per chunk
CHUNK_OVERLAP = 50      # tokens shared between consecutive chunks

# Retrieval
TOP_K = 3               # number of chunks sent to the LLM