import os

from dotenv import load_dotenv
from fastapi import FastAPI, Body, HTTPException

from constants import ServicesNames
from services.registry_client import register_service
from text_processing import text_processor

load_dotenv()
app = FastAPI()


@app.post('/text_processing')
async def text_processing(enable_spell_checking: bool = False, body: dict[str, str] = Body(...)):
    if body.get('text') is None:
        raise HTTPException(status_code=422, detail="The attribute 'text' is required.")
    text = body['text']
    result = text_processor(text, enable_spell_checking)
    return {
        'result': result
    }


if __name__ == '__main__':
    import uvicorn

    host = os.getenv('HOST')
    port = os.getenv('TEXT_PROCESSING_PORT')
    register_service(name=ServicesNames.text_processing, port=port)
    uvicorn.run(app, host=host, port=int(port))
