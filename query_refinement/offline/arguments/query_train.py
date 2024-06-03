import os
import sqlite3
import pickle
import datetime

from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

from constants import query_pickle_folder_path, arguments_queries_vectorizer_file, \
    arguments_queries_tfidf_matrix_file, limit_docs, arguments_titles_tfidf_matrix_file, \
    arguments_titles_vectorizer_file
from services.text_processing.text_processing import text_processor

# Ignore warning to use custom tokenizer
import warnings

warnings.filterwarnings('ignore',
                        message="The parameter 'token_pattern' will not be used since 'tokenizer' is not None")


def fetch_docs_titles():
    connection = sqlite3.connect('../../../sql.db')
    cursor = connection.cursor()
    print(f'Fetching titles... (at {datetime.datetime.now()})')

    if limit_docs:
        query = 'SELECT title FROM arguments LIMIT ?'
        docs_titles = cursor.execute(query, (limit_docs,)).fetchall()
    else:
        docs_titles = cursor.execute('SELECT title FROM arguments').fetchall()

    docs_titles = [row[0] for row in docs_titles]

    print(f'_____ Titles fetched successfully at {datetime.datetime.now()} _____')

    cursor.close()
    connection.close()

    return docs_titles


def fetch_queries():
    connection = sqlite3.connect('../../data_loaders/queries.db')
    cursor = connection.cursor()
    print(f'Fetching queries... (at {datetime.datetime.now()})')

    db_queries = cursor.execute('SELECT title, description, narrative FROM arguments_queries').fetchall()

    merged_queries = []
    for title, description, narrative in db_queries:
        parts = [title, description, narrative]
        merged_query = ' '.join(parts)
        merged_queries.append(merged_query)

    print(f'_____ Queries fetched successfully at {datetime.datetime.now()} _____')

    cursor.close()
    connection.close()

    return merged_queries


def titles_text_processing(titles_list):
    print(f'Start Titles Text processing... (at {datetime.datetime.now()})')

    processed_titles = [text_processor(title) for title in titles_list]

    print(f'_____ Titles Text Processing finished successfully at {datetime.datetime.now()} _____')

    return processed_titles


def queries_text_processing(queries_list):
    print(f'Start Queries Text processing... (at {datetime.datetime.now()})')

    processed_queries = [text_processor(query) for query in queries_list]

    print(f'_____ Queries Text Processing finished successfully at {datetime.datetime.now()} _____')

    return processed_queries


def queries_train():
    queries = queries_text_processing(fetch_queries())

    print(f'Start Queries Indexing... (at {start_time})')

    vectorizer = TfidfVectorizer(tokenizer=word_tokenize)
    tfidf_matrix = vectorizer.fit_transform(queries)

    print(f'_____ Queries Indexing finished successfully at {datetime.datetime.now()} _____')

    print(f'Dumping the query pickle file... (at {datetime.datetime.now()})')

    if not os.path.exists(query_pickle_folder_path):
        os.makedirs(query_pickle_folder_path)

    with open(arguments_queries_vectorizer_file, "wb") as f:
        pickle.dump(vectorizer, f)

    with open(arguments_queries_tfidf_matrix_file, "wb") as f:
        pickle.dump(tfidf_matrix, f)

    print(f'_____ The query pickle files dumped successfully at {datetime.datetime.now()} _____')


def titles_train():
    titles = titles_text_processing(fetch_docs_titles())

    print(f'Start Titles Indexing... (at {datetime.datetime.now()})')

    vectorizer = TfidfVectorizer(tokenizer=word_tokenize)
    tfidf_matrix = vectorizer.fit_transform(titles)
    print(f'_____ Titles Indexing finished successfully at {datetime.datetime.now()} _____')

    print(f'Dumping the titles pickle file... (at {datetime.datetime.now()})')

    if not os.path.exists(query_pickle_folder_path):
        os.makedirs(query_pickle_folder_path)

    with open(arguments_titles_vectorizer_file, "wb") as f:
        pickle.dump(vectorizer, f)

    with open(arguments_titles_tfidf_matrix_file, "wb") as f:
        pickle.dump(tfidf_matrix, f)

    print(f'_____ The titles pickle files dumped successfully at {datetime.datetime.now()} _____')


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    queries_train()
    titles_train()

    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print(f'Finished in time: {elapsed_time}')
