from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, VectorStoreIndex, Document
from llama_index.readers.mongodb import SimpleMongoReader
from database.database import MongoDBRepository
from vectorstore.vectore_store import StorageContextCreator
from config.config import mongo_url



context_creator = StorageContextCreator()
mongo = MongoDBRepository()

about_docs_context = context_creator.create_context('AboutCG')
sales_docs_context = context_creator.create_context('Sales')
operations_docs_context = context_creator.create_context('Operations')
Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-base-en-v1.5"
    )

def create_indexing(context, mongo_collection_name):
    reader = SimpleMongoReader(
        host="mongodb://mongodb",
        port=27017,
        uri=mongo_url
    )

    documents = reader.load_data(
        db_name="AboutCG",
        collection_name=mongo_collection_name,
        field_names=["text"],
        metadata_names=["_id"]
    )

    new_docs = []

    for doc in documents:
        doc_id = str(doc.metadata["_id"])
        new_doc = Document(doc_id=doc_id,text=doc.text)
        new_docs.append(new_doc)

    return VectorStoreIndex.from_documents(new_docs, storage_context=context)
def listen_to_change_stream(collection, index, collection_name):
    while True:
        try:
            print(f"Attempting to watch change stream for {collection_name}")
            with collection.watch() as stream:
                for change in stream:
                    if change['operationType'] in ['insert', 'update', 'delete']:
                        print(f"Change detected in {collection_name}: {change['operationType']}")
                        
                        # Reload documents
                        reader = SimpleMongoReader(
                            host="mongodb://mongodb",
                            port=27017,
                            uri=mongo_url
                        )
                        documents = reader.load_data(
                            db_name="AboutCG",
                            collection_name=collection_name,
                            field_names=["text"],
                            metadata_names=["_id"]
                        )
                        
                        new_docs = []
                        for doc in documents:
                            doc_id = str(doc.metadata["_id"])
                            new_doc = Document(doc_id=doc_id, text=doc.text)
                            new_docs.append(new_doc)
                        
                        # Use persist method instead of refresh
                        if new_docs:
                            try:
                                # Try using persist method
                                index.insert_nodes(new_docs)
                                print(f"Successfully updated index for {collection_name}")
                            except Exception as persist_error:
                                print(f"Error persisting documents: {persist_error}")
        
        except Exception as e:
            print(f"Error in change stream for {collection_name}: {e}")
            
            # Exponential backoff
            import time
            time.sleep(5)  # Wait before retry
def main():
    index1 = create_indexing(about_docs_context, "Docs")
    index2 = create_indexing(sales_docs_context, "SalesDocs")
    index3 = create_indexing(operations_docs_context, "OperationsDocs")
    col1 = mongo.get_collection("Docs")
    col2 = mongo.get_collection("SalesDocs")
    col3 = mongo.get_collection("OperationsDocs")

    from threading import Thread
    
    t1 = Thread(target=listen_to_change_stream, args=(col1, index1, "Docs"), daemon=True)
    t2 = Thread(target=listen_to_change_stream, args=(col2, index2, "SalesDocs"), daemon=True)
    t3 = Thread(target=listen_to_change_stream, args=(col3, index3, "OperationsDocs"), daemon=True)
    
    t1.start()
    t2.start()
    t3.start()
    
    # Prevent main thread from exiting
    t1.join()
    t2.join()
    t3.join()

if __name__ == "__main__":
        main()
