from pymongo import MongoClient

class MongoDBRepository:
    def __init__(self, db_url):
        self.mongo_client = MongoClient(db_url)
        self.db = self.mongo_client['AboutCG']
        

    def get_collection(self, collection_name: str):
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)
        collection = self.db[collection_name]
        return collection

    def close(self):
        self.mongo_client.close()

    def insert_data(self, data, collection):
        # Create document with the specified structure
        document = {
            "text": data["text"]
        }
        # Insert formatted data into MongoDB
        result = collection.insert_one(document)
        
        return result.acknowledged