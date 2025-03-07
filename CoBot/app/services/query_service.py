from app.repository.query_repository import QueryRepository

class QueryService():

    def __init__(self) -> None:
        self.repo = QueryRepository()

    def process_query(self, query: str, index, template=None):
        
           return self.repo.rag_handler(query, index, template)
        
