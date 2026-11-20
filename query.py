import argparse

import chromadb
from chromadb.config import Settings
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

import config


def main():
    parser = argparse.ArgumentParser(description="Ask a question about the indexed documents.")
    parser.add_argument("question", help="question to ask")
    args = parser.parse_args()

    # Reconnect to the existing index (no re-indexing)
    db = chromadb.PersistentClient(
        path=str(config.CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )
    collection = db.get_or_create_collection(config.COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=collection)
    embed_model = OllamaEmbedding(model_name=config.EMBED_MODEL, base_url=config.OLLAMA_URL)
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

    # Local LLM that writes the answer
    llm = Ollama(model=config.LLM_MODEL, base_url=config.OLLAMA_URL, request_timeout=config.REQUEST_TIMEOUT)
    query_engine = index.as_query_engine(llm=llm, similarity_top_k=config.TOP_K)

    # 4. Querying: embed question, retrieve closest chunks, generate answer
    response = query_engine.query(args.question)
    print(f"\nAnswer:\n{response}\n")

    # Chunks used to build the answer
    print("Sources:")
    for node in response.source_nodes:
        print(f"  - {node.metadata.get('file_name')} (score: {node.score:.2f})")


if __name__ == "__main__":
    main()