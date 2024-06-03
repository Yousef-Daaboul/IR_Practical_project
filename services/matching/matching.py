from sqlite3 import Connection
from typing import List

import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity

from constants import ServicesNames
from services.registry_client import get_service


def get_query_vector(text: str, dataset_id: int, with_process_text: bool = True):
    url = get_service(ServicesNames.indexing)
    data = {
        'text': text,
        'with_process_text': with_process_text
    }
    result = requests.post(url=f'{url}/{dataset_id}', json=data)
    result.raise_for_status()
    return result.json()['result']


def match(query_vector, matrix):
    similarity_scores = cosine_similarity(query_vector, matrix).flatten()
    sorted_indices = np.argsort(similarity_scores)[::-1]
    ranked_indices = sorted_indices[:10]
    ranked_indices = [num + 1 for num in ranked_indices]
    return ranked_indices


def get_from_db(sqlite_connection: Connection, clean_connection: Connection, dataset_id: int, indices):
    if dataset_id == 1:
        table_name = 'clinical_trials'
        query = f'SELECT * FROM {table_name} where id in {tuple(indices)}'
        order = indices
    else:
        table_name = 'arguments'
        cursor_cleaned = clean_connection.cursor()
        cleaned_table_name = 'clean_arguments'
        doc_ids = cursor_cleaned.execute(
            f'SELECT doc_id from {cleaned_table_name} where id in {tuple(indices)}'
        ).fetchall()
        doc_ids = [item[0] for item in doc_ids]
        query = f'SELECT * FROM {table_name} where doc_id in {tuple(doc_ids)} limit {len(doc_ids)}'
        order = doc_ids

    cursor = sqlite_connection.cursor()

    query_result = cursor.execute(query).fetchall()
    result = convert_to_json(dataset_id, query_result)
    data = sort_dicts_by_list(result, order, dataset_id)
    cursor.close()
    return data


def sort_dicts_by_list(data, order, dataset_id):
    """Sorts a list of dictionaries based on the order of a corresponding list of numbers.

    Args:
        data: A list of dictionaries, where each dictionary has an 'id' key.
        order: A list of numbers that defines the desired order for the dictionaries.

    Returns:
        A new list containing the sorted dictionaries.

    Raises:
        TypeError: If the lengths of 'data' and 'order' are not equal.
        ValueError: If any element in 'order' is not found in the 'id' values of 'data'.
    """
    print(f'len(data) : {len(data)} ')
    print(f'len(order) : {len(order)} ')
    if len(data) != len(order):
        raise TypeError("Lengths of data and order lists must be equal.")

    if dataset_id == 1:
        id_to_dict = {d['id']: d for d in data}  # Create a dictionary for efficient lookup
    else:
        id_to_dict = {d['doc_id']: d for d in data}

    if not all(num in id_to_dict for num in order):
        raise ValueError(f"Values in 'order' not found in any dictionary 'id'.")

    sorted_data = [id_to_dict[num] for num in order]

    return sorted_data


def convert_to_json(dataset_id: int, data: List[tuple]) -> List[dict]:
    if dataset_id == 1:
        desired_structure = {'id': None, 'doc_id': None, 'title': None, 'detailed_description': None, 'summary': None,
                             'eligibility': None, 'keywords': None}
    else:
        desired_structure = {'id': None, 'doc_id': None, 'title': None, 'description': None, 'conclusion': None,
                             'mode': None, 'premise': None}

    converted_data = [
        dict(zip(desired_structure.keys(), item))
        for item in data
    ]
    return converted_data


def process_text(text: str, with_correct_spelling: bool = False) -> str:
    url = get_service(ServicesNames.text_processing)
    params = {'enable_spell_checking': with_correct_spelling}
    data = {
        'text': text,
    }
    result = requests.post(url=url, json=data, params=params)
    return result.json()['result']


def register_query(dataset_id: int, query: str):
    url = get_service(ServicesNames.query_register)
    params = {'dataset_id': dataset_id, 'query': query}

    result = requests.post(url=url, params=params)
    return result.json()


def query_expansion(query: str, with_text_process: bool) -> str:
    url = get_service(ServicesNames.query_expansion)
    params = {'with_text_process': with_text_process, 'query': query}

    result = requests.get(url=url, params=params)
    return result.json()['expanded_query']
