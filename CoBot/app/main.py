from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router.api import router
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.llms.nvidia import NVIDIA
from contextlib import asynccontextmanager
from app.config.config import api_key, mongo


# Load documents and create index at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-base-en-v1.5"
    )
    Settings.llm = NVIDIA(model= "nv-mistralai/mistral-nemo-12b-instruct",nvidia_api_key=api_key,base_url="https://integrate.api.nvidia.com/v1")

    yield
    mongo.close()


app = FastAPI(lifespan=lifespan)
# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.coguide.in","https://www.coguide.in/","https://coguide.in","*.coguide.in"],  # Frontend origin
    allow_credentials=True,  # Allow cookies or other credentials
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router)


