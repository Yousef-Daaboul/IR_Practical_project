import os
import sqlite3
import pickle
import datetime

from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

from services.text_processing.text_processing import text_processor

from constants import clinical_trials_vectorizer_file, clinical_trials_tfidf_matrix_file, pickles_folder_path, \
    limit_docs

# # this for ignore warning to use custom tokenizer
import warnings

warnings.filterwarnings('ignore',
                        message="The parameter 'token_pattern' will not be used since 'tokenizer' is not None'")

if __name__ == '__main__':
    sqliteConnection = sqlite3.connect('../../sql.db')
    cursor = sqliteConnection.cursor()
    print(f'Fetching docs...(at {datetime.datetime.now()})')

    if limit_docs:
        query = 'SELECT description FROM clinical_trials LIMIT ?'
        docs = cursor.execute(query, (limit_docs,)).fetchall()
    else:
        docs = cursor.execute('SELECT description FROM clinical_trials').fetchall()

    # `fetchall` function return (list of tuple of str) so we do that to make it (list of str)
    docs = [row[0] for row in docs]

    print(f'_____ Docs fetched successfully at {datetime.datetime.now()} _____')

    print(f'Start Text processing...(at {datetime.datetime.now()})')
    docs = [text_processor(doc) for doc in docs]
    print(f'_____ Text Processing finished successfully at {datetime.datetime.now()} _____')

    print(f'Start Indexing...(at {datetime.datetime.now()})')
    vectorizer = TfidfVectorizer(tokenizer=word_tokenize)
    tfidf_matrix = vectorizer.fit_transform(docs)
    print(f'_____ Indexing finished successfully at {datetime.datetime.now()} _____')

    print(f'Dumping the pickle file...(at {datetime.datetime.now()})')

    # this for creating pickle_files folder
    if not os.path.exists(pickles_folder_path):
        os.makedirs(pickles_folder_path)

    with open(clinical_trials_vectorizer_file, "wb") as f:
        pickle.dump(vectorizer, f)

    with open(clinical_trials_tfidf_matrix_file, "wb") as f:
        pickle.dump(tfidf_matrix, f)
    print(f'_____ The pickle files dumped successfully at {datetime.datetime.now()} _____')