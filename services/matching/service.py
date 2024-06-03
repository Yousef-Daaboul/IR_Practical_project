import os
import sqlite3
from sqlite3 import Connection
import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from constants import load_pickle_file, arguments_tfidf_matrix_file, ServicesNames, \
    clinical_trials_main_matrix_file, clinical_docs_sqlite_db_path, arguments_docs_sqlite_db_path, \
    cleaned_arguments_docs_sqlite_db_path
from services.matching.matching import get_query_vector, match, get_from_db, process_text, register_query, \
    query_expansion
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


@app.get('/matching/{dataset_id}')
async def matching(dataset_id: int, query: str):
    if query.strip() == '':
        raise HTTPException(status_code=400, detail="The query param 'query' is required")

    if dataset_id == 1:
        matrix = clinical_matrix
        connection = clinical_sqlite_connection
        clean_connection = None
    elif dataset_id == 2:
        matrix = arguments_matrix
        connection = arguments_sqlite_connection
        clean_connection = cleaned_arguments_sqlite_connection
    else:
        raise HTTPException(status_code=422, detail='path param must be 1 for clinical or 2 for arguments.')

    start_time = datetime.datetime.now()

    # First Process Text
    cleaned_text = process_text(query, True)
    print(f'cleaned_text: {cleaned_text}')
    if cleaned_text == '':
        return {'data': []}
    # Second register query in logs
    query_id = register_query(dataset_id, cleaned_text)['query_id']
    # Third query expansion
    cleaned_text = query_expansion(cleaned_text, False)
    print(f'Query expanded {cleaned_text}')
    # Fourth reCleaned Text
    # cleaned_text = process_text(cleaned_text, False)
    # print(f'cleaned_text: {cleaned_text}')

    query_vector = get_query_vector(cleaned_text, dataset_id, False)
    indices = match(query_vector, matrix)
    print(f'indices: {indices}')
    data = get_from_db(connection, clean_connection, dataset_id, indices)

    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print(f'Finished in time: {elapsed_time}')

    return {'data': data, 'query_id': query_id}


if __name__ == '__main__':
    import uvicorn

    host = os.getenv('HOST')
    port = os.getenv('MATCHING_PORT')
    register_service(name=ServicesNames.matching, port=port)

    clinical_matrix = load_pickle_file(clinical_trials_main_matrix_file)
    arguments_matrix = load_pickle_file(arguments_tfidf_matrix_file)

    clinical_sqlite_connection: Connection = sqlite3.connect(clinical_docs_sqlite_db_path)
    arguments_sqlite_connection: Connection = sqlite3.connect(arguments_docs_sqlite_db_path)
    cleaned_arguments_sqlite_connection: Connection = sqlite3.connect(cleaned_arguments_docs_sqlite_db_path)

    uvicorn.run(app, host=host, port=int(port))
