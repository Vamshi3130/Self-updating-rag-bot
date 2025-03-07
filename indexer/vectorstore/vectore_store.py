import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from config.config import Chroma_host, chroma_port

client = chromadb.HttpClient(
            host= Chroma_host,  # service name in docker-compose
            port= chroma_port  # Internal port in container
        )

class StorageContextCreator():
    def __init__(self) -> None:
       pass

    def create_context(self, collection_name: str) -> StorageContext:
        collection = client.get_or_create_collection(collection_name)
        vectore_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vectore_store)
        return storage_context