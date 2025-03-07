import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from app.config.config import chroma_host, chroma_port


client = chromadb.HttpClient(
            host= chroma_host,  # service name in docker-compose
            port= chroma_port  # Internal port in container
        )

class StorageGetterChroma():
    def __init__(self) -> None:
       pass

    def get_store(self, collection_name: str):
        collection = client.get_or_create_collection(collection_name)
        vectore_store = ChromaVectorStore(chroma_collection=collection) 
        return vectore_store
