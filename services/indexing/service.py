import os

from dotenv import load_dotenv
from fastapi import FastAPI, Body, HTTPException

from constants import load_pickle_file, arguments_vectorizer_file, ServicesNames, clinical_trials_main_vectorizer_file
from services.indexing.indexing import vectorize_text, process_text
from services.registry_client import register_service

load_dotenv()
app = FastAPI()


@app.post('/indexing/{dataset_id}')
async def indexing(dataset_id: int, body: dict[str, str] = Body(...)):
    if body.get('text') is None:
        raise HTTPException(status_code=422, detail="The attribute 'text' is required.")
    cleaned_text = body['text']
    if body['with_process_text'] is True:
        cleaned_text = process_text(cleaned_text)

    if dataset_id == 1:
        result = vectorize_text(clinical_vectorizer, cleaned_text)
    elif dataset_id == 2:
        result = vectorize_text(arguments_vectorizer, cleaned_text)
    else:
        raise HTTPException(status_code=422, detail='Path param must be 1 for clinical or 2 for arguments.')

    return {
        'result': result,
    }


if __name__ == '__main__':
    import uvicorn

    clinical_vectorizer = load_pickle_file(clinical_trials_main_vectorizer_file)
    arguments_vectorizer = load_pickle_file(arguments_vectorizer_file)

    host = os.getenv('HOST')
    port = os.getenv('INDEXING_PORT')
    register_service(name=ServicesNames.indexing, port=port)
    uvicorn.run(app, host=host, port=int(port))
