import sqlite3


def init_arguments_table():
    query = '''
            create table arguments
            (
                id          integer not null
                    constraint arguments_pk
                        primary key autoincrement,
                doc_id      TEXT,
                title       TEXT,
                description TEXT,
                conclusion  TEXT
            );
            
            create index arguments_id_index
                on arguments (id);
            
    '''
    cursor.execute(query)


def init_clinical_table():
    query = '''
            create table clinical_trials
            (
                id          integer not null
                    constraint clinical_trials_pk
                        primary key autoincrement,
                doc_id      TEXT
                    constraint clinical_trials_pk_2
                        unique,
                title       TEXT,
                description TEXT,
                summary     TEXT
            );
            
            create index clinical_trials_id_index
                on clinical_trials (id);
    '''
    cursor.execute(query)


if __name__ == '__main__':
    sqliteConnection = sqlite3.connect('../sql.db')
    cursor = sqliteConnection.cursor()
    init_clinical_table()
    init_arguments_table()
