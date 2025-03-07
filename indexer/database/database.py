from pymongo import MongoClient
from config.config import mongo_url

class MongoDBRepository:
    def __init__(self):
        self.mongo_client = MongoClient(mongo_url)
        self.db = self.mongo_client['AboutCG']
        

    def get_collection(self, collection_name: str):
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)
        collection = self.db[collection_name]
        return collection

    def close(self):
        self.mongo_client.close()
