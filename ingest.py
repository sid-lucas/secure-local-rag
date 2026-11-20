import argparse
from pathlib import Path

import chromadb
from chromadb.config import Settings
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

import config


def main():
    parser = argparse.ArgumentParser(description="Index documents into the local vector store.")
    parser.add_argument("--source", type=Path, default=config.DATA_DIR, help="folder with documents to index")
    parser.add_argument("--reset", action="store_true", help="delete the existing index before indexing")
    args = parser.parse_args()

    # 1. Loading: read every file in the source folder
    documents = SimpleDirectoryReader(str(args.source), recursive=True).load_data()
    print(f"Loaded {len(documents)} documents from {args.source}")

    # 3. Storing: local Chroma database, telemetry disabled
    db = chromadb.PersistentClient(
        path=str(config.CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )
    if args.reset:
        try:
            db.delete_collection(config.COLLECTION_NAME)
        except Exception:
            pass  # collection did not exist yet
    collection = db.get_or_create_collection(config.COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=collection)

    # 2. Indexing: split into chunks, embed each chunk, write to Chroma
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=512, chunk_overlap=64),
            OllamaEmbedding(model_name=config.EMBED_MODEL, base_url=config.OLLAMA_URL),
        ],
        vector_store=vector_store,
    )
    nodes = pipeline.run(documents=documents)
    print(f"Stored {len(nodes)} chunks in {config.CHROMA_DIR}")


if __name__ == "__main__":
    main()