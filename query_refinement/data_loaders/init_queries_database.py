import sqlite3


def init_arguments_queries_table():
    queries = [
        '''
        CREATE TABLE arguments_queries
        (
            id          INTEGER NOT NULL
                CONSTRAINT arguments_queries_pk
                    PRIMARY KEY AUTOINCREMENT,
            query_id      TEXT
                CONSTRAINT arguments_queries_pk_2
                    UNIQUE,
            title       TEXT,
            description       TEXT,
            narrative       TEXT
        );
        ''',
        '''
        CREATE INDEX arguments_queries_id_index
            ON arguments_queries (id);
        '''
    ]
    for query in queries:
        cursor.execute(query)


def init_clinical_queries_table():
    queries = [
        '''
        CREATE TABLE clinical_queries
        (
            id          INTEGER NOT NULL
                CONSTRAINT clinical_queries_pk
                    PRIMARY KEY AUTOINCREMENT,
            query_id      TEXT
                CONSTRAINT clinical_queries_pk_2
                    UNIQUE,
            disease TEXT,
            gene TEXT,
            demographic TEXT,
            other TEXT
        );
        ''',
        '''
        CREATE INDEX clinical_queries_id_index
            ON clinical_queries (id);
        '''
    ]
    for query in queries:
        cursor.execute(query)


if __name__ == '__main__':
    sqliteConnection = sqlite3.connect('./queries.db')
    cursor = sqliteConnection.cursor()
    init_clinical_queries_table()
    init_arguments_queries_table()
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()
