from fastapi import  HTTPException, APIRouter
from app.services.query_service import QueryService
from llama_index.core import VectorStoreIndex, PromptTemplate
from app.vectorstore.vectore_store import StorageGetterChroma


context_creator = StorageGetterChroma()


router = APIRouter(prefix='/v1')



@router.post("/query")
async def query_endpoint(query: dict):
   
    try:
        _service = QueryService()
        shared_context = context_creator.get_store("AboutCG")  # Make sure collection name matches

        # Load or create index
        index = VectorStoreIndex.from_vector_store(shared_context)
        response = _service.process_query(query['content'],index=index)  # Pass index to process_query
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/salesquery")
async def query_endpoint(query: dict):
   
    try:
        _service = QueryService()
        shared_context = context_creator.get_store("Sales")  # Make sure collection name matches

        # Load or create index
        index = VectorStoreIndex.from_vector_store(shared_context)
        if 'generate' in query["content"].lower() or 'create email' in query["content"].lower():
            text_qa_template_str = (
            "Introduce the company's products or services to the client."
            " Context information is below.\n---------------------\n{context_str}\n---------------------\n"
            " Using the context information, write an engaging and persuasive email to the client based on the query: {query_str}\n"
        )
        else:
            text_qa_template_str = (
            "As a sales assistant, provide clear and concise information about the product's features, benefits, and pricing."
            " Context information is below.\n---------------------\n{context_str}\n---------------------\n"
            " Answer based on the query: {query_str}\n"
        )
    
        text_qa_template = PromptTemplate(text_qa_template_str)

        response = _service.process_query(query['content'], index=index, template=text_qa_template)  # Pass index and template as keyword args
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/operationsquery")
async def query_endpoint(query: dict):
   
    try:
        _service = QueryService()
        shared_context = context_creator.get_store("Operations")  # Make sure collection name matches

        # Load or create index
        index = VectorStoreIndex.from_vector_store(shared_context)
        print(query)
        response = _service.process_query(query['content'],index )  # Pass index to process_query
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

