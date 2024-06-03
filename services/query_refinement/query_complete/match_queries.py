import sqlite3
from sqlite3 import Connection
from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from constants import load_pickle_file, clinical_queries_vectorizer_file, arguments_queries_vectorizer_file, \
    clinical_queries_tfidf_matrix_file, arguments_queries_tfidf_matrix_file, queries_sqlite_db_path, ServicesNames


def match_queries(cleaned_text, dataset_id):
    query_vector = get_query_vector(cleaned_text, dataset_id)

    if dataset_id == 1:
        matrix = load_pickle_file(clinical_queries_tfidf_matrix_file)
    else:
        matrix = load_pickle_file(arguments_queries_tfidf_matrix_file)

    indices = match(query_vector, matrix)
    if indices is not None:
        queries_sqlite_connection: Connection = sqlite3.connect(queries_sqlite_db_path)
        return get_from_db(queries_sqlite_connection, dataset_id, indices)
    else:
        return []


def match(query_vector, matrix, threshold=0.1):
    similarity_scores = cosine_similarity(query_vector, matrix).flatten()
    max_similarity = np.max(similarity_scores)

    # if max_similarity < threshold:
    #     return None

    sorted_indices = np.argsort(similarity_scores)[::-1]
    ranked_indices = sorted_indices[:10]
    ranked_indices = [num + 1 for num in ranked_indices]
    return ranked_indices


def get_query_vector(cleaned_text: str, dataset_id: int):
    if dataset_id == 1:
        query_vectorizer = load_pickle_file(clinical_queries_vectorizer_file)
    else:
        query_vectorizer = load_pickle_file(arguments_queries_vectorizer_file)

    return vectorize_text(query_vectorizer, cleaned_text)


def vectorize_text(vectorizer: TfidfVectorizer, text: str):
    vector = vectorizer.transform([text])
    return vector.toarray().tolist()


def get_from_db(db: Connection, dataset_id: int, indices):
    if dataset_id == 1:
        query_table_name = 'clinical_queries'
    else:
        query_table_name = 'arguments_queries'

    cursor = db.cursor()
    query_result = cursor.execute(f'SELECT * FROM {query_table_name} where id in {tuple(indices)}').fetchall()
    result = convert_to_json(dataset_id, query_result)
    data = sort_dicts_by_list(result, indices)
    cursor.close()
    return data


def sort_dicts_by_list(data, order):
    if len(data) != len(order):
        raise TypeError("Lengths of data and order lists must be equal.")

    id_to_dict = {d['id']: d for d in data}  # Create a dictionary for efficient lookup

    if not all(num in id_to_dict for num in order):
        raise ValueError(f"Values in 'order' not found in any dictionary 'id'.")

    sorted_data = [id_to_dict[num] for num in order]

    return sorted_data


def convert_to_json(dataset_id: int, data: List[tuple]) -> List[dict]:
    if dataset_id == 1:
        desired_structure = {'id': None, 'query_id': None, 'disease': None, 'gene': None, 'demographic': None,
                             'other': None}
    else:
        desired_structure = {'id': None, 'query_id': None, 'title': None, 'description': None, 'narrative': None}

    converted_data = [
        dict(zip(desired_structure.keys(), item))
        for item in data
    ]
    return converted_data
