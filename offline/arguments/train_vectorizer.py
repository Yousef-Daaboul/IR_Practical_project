import sqlite3
import pickle
import datetime

import numpy as np
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

from constants import load_pickle_file, arguments_main_vectorizer_file

def get_main_vectorizer(cursor):
    print(f'Fetching all...(at {datetime.datetime.now()})')
    docs = cursor.execute(
        'SELECT title || " " || summary || " " || description as name FROM clinical_trials').fetchall()

    # `fetchall` function return (list of tuple of str) so we do that to make it (list of str)
    docs = [row[0] for row in docs]

    print(f'_____ Docs fetched successfully at {datetime.datetime.now()} _____')
    print(f'Start Indexing all...(at {datetime.datetime.now()})')
    main_vectorizer = TfidfVectorizer(tokenizer=word_tokenize)
    all_tfidf_matrix = main_vectorizer.fit_transform(docs)
    print(f'_____ Indexing finished successfully at {datetime.datetime.now()} _____')
    print(f'Dumping the pickle file (main_vectorizer)...(at {datetime.datetime.now()})')
    with open(arguments_main_vectorizer_file, "wb") as f:
        pickle.dump(main_vectorizer, f)
    return main_vectorizer

def get_title_matrix(cursor, main_vectorizer):
    print(f'Fetching all...(at {datetime.datetime.now()})')
    docs = cursor.execute()
    docs = cursor.execute('SELECT title FROM arguments')
    docs = [row[0] for row in docs]
    print(f'_____ Docs fetched successfully at {datetime.datetime.now()} _____')
    print(f'Start Indexing title...(at {datetime.datetime.now()})')
    title_matrix = main_vectorizer.transform(docs)
    return title_matrix

def get_description_matrix(cursor, main_vectorizer):
    print(f'Fetching all...(at {datetime.datetime.now()})')
    docs = cursor.execute('SELECT description FROM arguments').fetchall()
    docs = [row[0] for row in docs]
    print(f'_____ Docs fetched successfully at {datetime.datetime.now()} _____')
    print(f'Start Indexing description...(at {datetime.datetime.now()})')
    description_matrix = main_vectorizer.transform(docs)
    return description_matrix
def get_mode_matrix(cursor, main_vectorizer):
    print(f'Fetching all...(at {datetime.datetime.now()})')
    docs = cursor.execute('SELECT mode FROM arguments').fetchall()
    docs = [row[0] for row in docs]
    print(f'_____ Docs fetched successfully at {datetime.datetime.now()} _____')
    print(f'Start Indexing mode...(at {datetime.datetime.now()})')
    mode_matrix = main_vectorizer.transform(docs)
    return mode_matrix

def get_patient_matrix(cursor, main_vectorizer):
    print(f'Fetching all...(at {datetime.datetime.now()})')
    docs = cursor.execute('SELECT patient FROM arguments').fetchall()
    docs = [row[0] for row in docs]
    print(f'_____ Docs fetched successfully at {datetime.datetime.now()} _____')
    print(f'Start Indexing patient...(at {datetime.datetime.now()})')
    patient_matrix = main_vectorizer.transform(docs)
    return patient_matrix

def get_citations_matrix(cursor, main_vectorizer):
    print(f'Fetching all...(at {datetime.datetime.now()})')
    docs = cursor.execute('SELECT citation FROM arguments').fetchall()
    docs = [row[0] for row in docs]
    print(f'_____ Docs fetched successfully at {datetime.datetime.now()} _____')
    print(f'Start Indexing citations...(at {datetime.datetime.now()})')
    citations_matrix = main_vectorizer.transform(docs)
    return citations_matrix
if __name__ == '__main__':
    # فتح الاتصال بقاعدة البيانات
    connection = sqlite3.connect("../../clean_arguments.db")
    cursor = connection.cursor()
    main_vectorizer = get_main_vectorizer(cursor)
    title_matrix = get_title_matrix(cursor, main_vectorizer)
    description_matrix = get_description_matrix(cursor, main_vectorizer)
    mode_matrix = get_mode_matrix(cursor, main_vectorizer)
    premise_matrix = get_patient_matrix(cursor, main_vectorizer)
    conclusion_matrix = get_citations_matrix(cursor, main_vectorizer)

    # Define weights for each matrix
    weights = {
        'title': 4,
        'description': 1,
        'premise': 3,
        'mode': 1,
        'conclusion': 2
    }

    # Compute the weighted sum of matrices directly using sparse matrices
    weighted_sum = (weights['title'] * title_matrix +
                    weights['description'] * description_matrix +
                    weights['premise'] * premise_matrix +
                    weights['mode'] * mode_matrix +
                    weights['conclusion'] * conclusion_matrix)

    total_weight = sum(weights.values())
    main_matrix = weighted_sum / total_weight
    print(f'Dumping the pickle file (main_matrix)...(at {datetime.datetime.now()})')
    with open("arguments_main_matrix.pickle", "wb") as f:
        pickle.dump(main_matrix, f)
    print(f'_____ The pickle files dumped successfully at {datetime.datetime.now()} _____')
