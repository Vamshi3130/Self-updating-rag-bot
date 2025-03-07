from dotenv import load_dotenv
import os 

load_dotenv()

Chroma_host = os.getenv("CHROMA_HOST")
chroma_port = os.getenv("CHROMA_PORT", 8000)
mongo_url = os.getenv("MONGODB_URI")

