from typing import List

from fastapi import (FastAPI, HTTPException, Body)

from service_registry.service import Service
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

services: List[Service] = []


@app.post("/services", status_code=201)
async def register_service(service_info: Service = Body()):
    if any((service.name == service_info.name and service.url == service_info.url) for service in services):
        return {'message': 'Service already registered'}
    services.append(service_info)
    print(services)
    return {"message": "Service registered successfully"}


@app.get("/services/{service_name}")
async def get_service_info(service_name: str):
    for service in services:
        if service.name == service_name:
            return service
    raise HTTPException(status_code=404, detail="Service not found")


if __name__ == '__main__':
    import uvicorn

    host = os.getenv('HOST')
    port = os.getenv('REGISTRY_PORT')
    uvicorn.run(app, host=host, port=int(port))
