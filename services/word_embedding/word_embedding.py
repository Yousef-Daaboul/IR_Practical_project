import os
from sqlite3 import Connection

import numpy as np
import requests
from nltk import word_tokenize

from constants import ServicesNames
from services.matching.matching import convert_to_json
from services.registry_client import get_service
from vector_store.clinical_vector_store import get_vector_store_index


def document_to_vector(doc, embedding_model, dimensions):
    vector = np.zeros(dimensions)  # Assuming n-dimensional GloVe vectors
    count = 0
    for word in doc:
        if word in embedding_model:
            vector += embedding_model[word]
            count += 1
    if count > 0:
        vector /= count
    return vector


def get_query_vector(cleaned_text, model_embedding, dimensions):
    return document_to_vector(word_tokenize(cleaned_text), model_embedding, dimensions)


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


def get_model_embedding(dataset_id):
    if dataset_id == 1:
        glove_file_path = os.path.join('..', '..', 'word_embedding', 'clinical_glove_model.txt')
    else:
        glove_file_path = os.path.join('..', '..', 'word_embedding', 'arguments_glove_model.txt')

    print(f'glove_file_path: {glove_file_path}')
    return load_glove_embeddings(glove_file_path)


def load_glove_embeddings(glove_file_path):
    emmbed_dict = {}

    with open(glove_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], 'float32')
            emmbed_dict[word] = vector

    return emmbed_dict


def match_query(query_vector, dataset_id, top_k):
    if dataset_id == 1:
        namespace = 'clinicaltrails'
        index_name = 'clinicaltrailscustomgloveindex'
    else:
        namespace = 'arguments'
        index_name = 'argumentscustomgloveindex'

    index = get_vector_store_index(index_name)
    return index.query(vector=query_vector.tolist(), top_k=top_k, namespace=namespace)


def get_from_db(sqlite_connection: Connection, dataset_id: int, doc_ids):
    if dataset_id == 1:
        table_name = 'clinical_trials'
    else:
        table_name = 'arguments'
    cursor = sqlite_connection.cursor()

    print(f'doc_ids : {doc_ids}')
    ids = [item['id'] for item in doc_ids]

    query_result = cursor.execute(f'SELECT * FROM {table_name} where doc_id in {tuple(ids)} Limit 10').fetchall()
    result = convert_to_json(dataset_id, query_result)
    print(f'result : {result}')
    print(f'ids : {ids}')
    data = sort_dicts_by_list(result, ids)
    cursor.close()
    return data


def sort_dicts_by_list(data, order):
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

    id_to_dict = {d['doc_id']: d for d in data}  # Create a dictionary for efficient lookup

    if not all(num in id_to_dict for num in order):
        raise ValueError(f"Values in 'order' not found in any dictionary 'id'.")

    sorted_data = [id_to_dict[num] for num in order]

    return sorted_data

