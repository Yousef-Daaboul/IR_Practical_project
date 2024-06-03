import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

from constants import ServicesNames
from services.query_refinement.expansion import expand_query
from services.query_refinement.query_logs import register_successful_query, register_query_logs
from services.query_refinement.auto_complete import match_queries, query_complete
from services.registry_client import register_service
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/auto_complete/{dataset_id}')
async def auto_complete(dataset_id: int, query: str):
    if query.strip() == '':
        raise HTTPException(status_code=400, detail="The query param 'query' is required")
    if dataset_id == 1 or dataset_id == 2:
        return query_complete(query, dataset_id, True)
    else:
        raise HTTPException(status_code=422, detail='path param must be 1 for clinical or 2 for arguments.')


@app.get('/query_expansion')
async def query_expansion(query: str, with_text_process: bool):
    if query.strip() == '':
        raise HTTPException(status_code=400, detail="The query is required")
    return expand_query(query, with_text_process)


@app.post('/query_register')
async def query_register(dataset_id: int, query: str):
    if query.strip() == '':
        raise HTTPException(status_code=400, detail="The query param 'query' is required")
    return register_query_logs(dataset_id, query)


class QueryData(BaseModel):
    dataset_id: int
    query_id: int


@app.post('/successful_query')
async def successful_query(data: QueryData):
    if data.query_id is None:
        raise HTTPException(status_code=400, detail="The query param 'query' is required")
    return register_successful_query(data.dataset_id, data.query_id)


if __name__ == '__main__':
    import uvicorn

    host = os.getenv('HOST')
    port = os.getenv('QUERY_REFINEMENT_PORT')
    register_service(name=ServicesNames.query_register, port=port)
    register_service(name=ServicesNames.query_expansion, port=port)
    uvicorn.run(app, host=host, port=int(port))
