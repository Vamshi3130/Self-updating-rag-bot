from llama_index.core import  VectorStoreIndex, PromptTemplate
from typing import Optional



class QueryRepository():
    def __init__(self) -> None:
         pass
    
    def rag_handler(self, query: str, index: VectorStoreIndex, prompt_template: Optional[PromptTemplate] = None):
        query_engine = index.as_query_engine(
            text_qa_template=prompt_template if prompt_template else None
        )
        response = query_engine.query(query)
        return response

    