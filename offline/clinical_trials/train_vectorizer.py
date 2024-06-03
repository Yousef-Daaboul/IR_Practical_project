import datetime
import pickle
import sqlite3

from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

from constants import clinical_trials_main_vectorizer_file, clinical_trials_main_matrix_file


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
    with open(clinical_trials_main_vectorizer_file, "wb") as f:
        pickle.dump(main_vectorizer, f)
    return main_vectorizer


def get_title_matrix(cursor, main_vectorizer):
    print(f'Fetching title...(at {datetime.datetime.now()})')
    docs = cursor.execute('SELECT title FROM clinical_trials')
    docs = [row[0] for row in docs]
    print(f'_____ Docs fetched successfully at {datetime.datetime.now()} _____')
    print(f'Start Indexing title...(at {datetime.datetime.now()})')
    title_matrix = main_vectorizer.transform(docs)
    return title_matrix


def get_description_matrix(cursor, main_vectorizer):
    print(f'Fetching description...(at {datetime.datetime.now()})')
    docs = cursor.execute('SELECT description FROM clinical_trials')
    docs = [row[0] for row in docs]
    print(f'_____ Docs fetched successfully at {datetime.datetime.now()} _____')
    print(f'Start Indexing description...(at {datetime.datetime.now()})')
    description_matrix = main_vectorizer.transform(docs)
    return description_matrix


def get_summary_matrix(cursor, main_vectorizer):
    print(f'Fetching summary...(at {datetime.datetime.now()})')
    docs = cursor.execute('SELECT summary FROM clinical_trials')
    docs = [row[0] for row in docs]
    print(f'_____ Docs fetched successfully at {datetime.datetime.now()} _____')
    print(f'Start Indexing summary...(at {datetime.datetime.now()})')
    summary_matrix = main_vectorizer.transform(docs)
    return summary_matrix


def get_eligibility_vectorizer(cursor, main_vectorizer):
    print(f'Fetching eligibility...(at {datetime.datetime.now()})')
    docs = cursor.execute('SELECT eligibility FROM clinical_trials')
    docs = [row[0] for row in docs]
    print(f'_____ Docs fetched successfully at {datetime.datetime.now()} _____')
    print(f'Start Indexing eligibility...(at {datetime.datetime.now()})')
    eligibility_matrix = main_vectorizer.transform(docs)
    print(f'Dumping the pickle file (eligibility_matrix)...(at {datetime.datetime.now()})')
    return eligibility_matrix


def get_condition_vectorizer(cursor, main_vectorizer):
    print(f'Fetching condition...(at {datetime.datetime.now()})')
    docs = cursor.execute('SELECT condition FROM clinical_trials')
    docs = [row[0] for row in docs]
    print(f'_____ Docs fetched successfully at {datetime.datetime.now()} _____')
    print(f'Start Indexing condition...(at {datetime.datetime.now()})')
    condition_matrix = main_vectorizer.transform(docs)
    return condition_matrix


def get_keyword_vectorizer(cursor, main_vectorizer):
    print(f'Fetching keywords...(at {datetime.datetime.now()})')
    docs = cursor.execute('SELECT keyword FROM clinical_trials')
    docs = [row[0] for row in docs]
    print(f'_____ Docs fetched successfully at {datetime.datetime.now()} _____')
    print(f'Start Indexing keywords...(at {datetime.datetime.now()})')
    keyword_matrix = main_vectorizer.transform(docs)
    return keyword_matrix


if __name__ == '__main__':
    sqliteConnection = sqlite3.connect('../../cleaned_clinicaltrials.db')
    cursor = sqliteConnection.cursor()
    main_vectorizer = get_main_vectorizer(cursor)
    title_matrix = get_title_matrix(cursor, main_vectorizer)
    description_matrix = get_description_matrix(cursor, main_vectorizer)
    summary_matrix = get_summary_matrix(cursor, main_vectorizer)
    eligibility_matrix = get_eligibility_vectorizer(cursor, main_vectorizer)
    condition_matrix = get_condition_vectorizer(cursor, main_vectorizer)
    keyword_matrix = get_keyword_vectorizer(cursor, main_vectorizer)

    # Ensure all matrices have the same shape
    assert title_matrix.shape == description_matrix.shape == summary_matrix.shape == eligibility_matrix.shape == keyword_matrix.shape, "Matrices do not have the same shape"

    # Define weights for each matrix
    weights = {
        'title': 0.6361868828516406,
        'description': 4.715457416712798,
        'summary': 0.12082601484510347,
        'eligibility': 3.706259895775634,
        'keyword': 6.759565033993937,
        'condition': 3.7190519036432876
    }

    # Compute the weighted sum of matrices directly using sparse matrices
    weighted_sum = (weights['title'] * title_matrix +
                    weights['description'] * description_matrix +
                    weights['summary'] * summary_matrix +
                    weights['eligibility'] * eligibility_matrix +
                    weights['keyword'] * keyword_matrix +
                    weights['condition'] * condition_matrix)

    total_weight = sum(weights.values())
    main_matrix = weighted_sum / total_weight

    print(f'Dumping the pickle file (main_matrix)...(at {datetime.datetime.now()})')
    with open(clinical_trials_main_matrix_file, "wb") as f:
        pickle.dump(main_matrix, f)
    print(f'_____ The pickle files dumped successfully at {datetime.datetime.now()} _____')

    cursor.close()
    sqliteConnection.close()
