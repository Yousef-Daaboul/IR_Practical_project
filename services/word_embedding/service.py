import os
import sqlite3
from sqlite3 import Connection
import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from constants import ServicesNames, clinical_docs_sqlite_db_path
from services.word_embedding.word_embedding import get_query_vector, process_text, get_model_embedding, match_query, \
    register_query, get_from_db
from services.registry_client import register_service

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/matching_word_embedding/{dataset_id}')
async def matching(dataset_id: int, query: str):
    if query.strip() == '':
        raise HTTPException(status_code=400, detail="The query param 'query' is required")

    if dataset_id == 1:
        model_embedding = clinical_model_embedding
        connection = clinical_sqlite_connection
    elif dataset_id == 2:
        model_embedding = arguments_model_embedding
        connection = clinical_sqlite_connection
    else:
        raise HTTPException(status_code=422, detail='path param must be 1 for clinical or 2 for arguments.')

    start_time = datetime.datetime.now()

    # First Process Text
    cleaned_text = process_text(query, True)
    print(f'cleaned_text: {cleaned_text}')
    if cleaned_text == '':
        return {'data': []}
    # Second register query in logs
    result = register_query(dataset_id, cleaned_text)
    print(f"register_query returned: {result}")

    query_vector = get_query_vector(cleaned_text, model_embedding, 300)

    results = match_query(query_vector, dataset_id, 10)

    data = get_from_db(connection, dataset_id, results['matches'])
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print(f'Finished in time: {elapsed_time}')

    return {'data': data, 'query_id': 'jj'}


if __name__ == '__main__':
    import uvicorn

    host = os.getenv('HOST')
    port = os.getenv('EMBEDDING_PORT')
    register_service(name=ServicesNames.matching_word_embedding, port=port)

    clinical_model_embedding = get_model_embedding(1)
    # arguments_model_embedding = get_model_embedding(2)
    arguments_model_embedding = 'jj'

    clinical_sqlite_connection: Connection = sqlite3.connect(clinical_docs_sqlite_db_path)

    uvicorn.run(app, host=host, port=int(port))
