import sqlite3
from sqlite3 import Error

from constants import query_logs_sqlite_db_path


def register_successful_query(dataset_id: int, query_id: int):
    """ increment the success_num column for a given query in the appropriate query_logs table """
    if dataset_id == 1:
        table_name = 'clinical_query_logs'
    elif dataset_id == 2:
        table_name = 'arguments_query_logs'
    else:
        print("Invalid dataset_id")
        return

    db_file = query_logs_sqlite_db_path
    conn = create_connection(db_file)

    if conn is not None:
        update_query_sql = f"""
            UPDATE {table_name}
            SET success_num = success_num + 1
            WHERE id = ?;
            """
        try:
            c = conn.cursor()
            c.execute(update_query_sql, (query_id,))
            conn.commit()
            return 'success'
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
    else:
        print("Error! Cannot create the database connection.")


def register_query_logs(dataset_id: int, query: str):
    """ register a new query in the appropriate query_logs table based on dataset_id """
    if dataset_id == 1:
        table_name = 'clinical_query_logs'
    elif dataset_id == 2:
        table_name = 'arguments_query_logs'
    else:
        print("Invalid dataset_id")
        return

    db_file = query_logs_sqlite_db_path
    conn = create_connection(db_file)

    if conn is not None:

        insert_query_sql = f"""
            INSERT OR IGNORE INTO {table_name} (query, success_num) 
            VALUES (?, 0);
            """
        try:
            c = conn.cursor()
            c.execute(insert_query_sql, (query,))
            conn.commit()
            # Fetch the query_id of the inserted or existing row
            select_query_id_sql = f"""
                       SELECT id FROM {table_name} WHERE query = ?;
                       """
            c.execute(select_query_id_sql, (query,))
            query_id = c.fetchone()[0]

            return {'success': True, 'query_id': query_id}
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
    else:
        print("Error! Cannot create the database connection.")


def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
