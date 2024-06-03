import os

import requests
from dotenv import load_dotenv

load_dotenv()
registry_url = os.getenv('REGISTRY_URL')


def register_service(name: str, port: str):
    load_dotenv()
    base_url = os.getenv('BASE_URL')

    service_info = {
        "name": name,
        "url": f"{base_url}:{port}/{name}"
    }
    response = requests.post(f'{registry_url}', json=service_info)
    response.raise_for_status()
    print(f'Service {name} registered successfully')
    print(response.json()['message'])


def get_service(name: str) -> str:
    response = requests.get(f'{registry_url}/{name}')
    response.raise_for_status()
    return response.json()['url']
