import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return connection


def init_clinical_query_logs_table(conn):
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS clinical_query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL UNIQUE,
            success_num INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
    create_index_sql = """
        CREATE INDEX IF NOT EXISTS cl_idx_query ON clinical_query_logs (query);
        """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        cursor.execute(create_index_sql)
        conn.commit()
    except Error as e:
        print(e)





def init_arguments_query_logs_table(conn):
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS arguments_query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL UNIQUE,
            success_num INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
    create_index_sql = """
        CREATE INDEX IF NOT EXISTS args_idx_query ON arguments_query_logs (query);
        """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        cursor.execute(create_index_sql)
        conn.commit()
    except Error as e:
        print(e)




if __name__ == '__main__':
    conn = create_connection('./query_logs.db')
    if conn is not None:
        try:
            init_clinical_query_logs_table(conn)
            init_arguments_query_logs_table(conn)
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")
