import pickle
from pathlib import Path

limit_docs = None

success_num = 1

current_script_path = Path(__file__).resolve()
project_root = current_script_path.parent

queries_sqlite_db_path = project_root / 'query_refinement/data_loaders/queries.db'
query_logs_sqlite_db_path = project_root / 'query_refinement/data_loaders/query_logs.db'
clinical_docs_sqlite_db_path = project_root / 'clinicaltrials.db'
arguments_docs_sqlite_db_path = project_root / 'argsme.db'
cleaned_arguments_docs_sqlite_db_path = project_root / 'clean_arguments.db'

pickles_folder_path = project_root / 'pickle_files'
query_pickle_folder_path = project_root / 'query_refinement/query_pickle_files'

clinical_queries_tfidf_matrix_file = query_pickle_folder_path / 'clinical_queries_tfidf_matrix.pickle'
clinical_titles_tfidf_matrix_file = query_pickle_folder_path / 'clinical_titles_tfidf_matrix.pickle'
clinical_queries_vectorizer_file = query_pickle_folder_path / 'clinical_queries_vectorizer.pickle'
clinical_titles_vectorizer_file = query_pickle_folder_path / 'clinical_titles_vectorizer.pickle'
arguments_queries_tfidf_matrix_file = query_pickle_folder_path / 'arguments_queries_tfidf_matrix.pickle'
arguments_titles_tfidf_matrix_file = query_pickle_folder_path / 'arguments_titles_tfidf_matrix.pickle'
arguments_queries_vectorizer_file = query_pickle_folder_path / 'arguments_queries_vectorizer.pickle'
arguments_titles_vectorizer_file = query_pickle_folder_path / 'arguments_titles_vectorizer.pickle'


# True
clinical_trials_queries_file = '../../pickle_files/clinical_trials/clinical_queries.pickle'
clinical_trials_qrels_file = '../../pickle_files/clinical_trials/clinical_trials_qrels.pickle'
clinical_trials_main_vectorizer_file = '../../pickle_files/clinical_trials/clinical_vectorizer.pickle'
clinical_trials_main_matrix_file = '../../pickle_files/clinical_trials/clinical_trials_main_matrix.pickle'
#######################################


argsme_qrels_file = '../../pickle_files/argsme/argsme_qrels.pickle'
argsme_queries_file = '../../pickle_files/argsme/argsme_queries.pickle'
arguments_tfidf_matrix_file = "../../pickle_files/argsme/arguments_main_matrix.pickle"
arguments_vectorizer_file = "../../pickle_files/argsme/arguments_vectorizer.pickle"


class ServicesNames:
    indexing = 'indexing'
    matching = 'matching'
    text_processing = 'text_processing'
    query_expansion = 'query_expansion'
    query_register = 'query_register'
    matching_word_embedding = 'matching_word_embedding'


def load_pickle_file(file: str):
    print(f'loading : {file}')
    try:
        with open(file, "rb") as f:
            data = pickle.load(f)
            f.close()
        return data
    except FileNotFoundError as e:
        print(e)
        return None
