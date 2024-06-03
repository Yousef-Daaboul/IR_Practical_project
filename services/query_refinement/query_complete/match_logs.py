import sqlite3
from sqlite3 import Error

from constants import query_logs_sqlite_db_path


def fetch_similar_queries(text: str, success_num: int, dataset_id):
    conn = create_connection(query_logs_sqlite_db_path)
    if conn is not None:
        try:
            c = conn.cursor()

            if dataset_id == 1:
                select_query_sql = """
                SELECT * FROM clinical_query_logs
                WHERE query LIKE ?
                AND success_num > ?
                ORDER BY success_num DESC;
                """
            else:
                select_query_sql = """
                SELECT * FROM arguments_query_logs
                WHERE query LIKE ?
                AND success_num > ?
                ORDER BY success_num DESC;
                """

            c.execute(select_query_sql, (f'%{text}%', success_num))
            results = c.fetchall()
            return results
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
    else:
        print("Error! Cannot create the database connection.")


def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file """
    connect = None
    try:
        connect = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return connect
