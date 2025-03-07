import os
from dotenv import load_dotenv
from app.database.database import MongoDBRepository



load_dotenv()
api_key = os.getenv('NVIDIA_API_KEY')
mongo_url = os.getenv('MONGODB_URI')
chroma_host = os.getenv('CHROMA_HOST')
chroma_port = os.getenv('CHROMA_PORT')
print(chroma_port)


mongo = MongoDBRepository(mongo_url)
