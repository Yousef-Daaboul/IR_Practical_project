import sqlite3
from json_parser import json_to_argument

DOCS_COUNT = 338620

DOCS_PATH = '/home/nezar/Desktop/datasets/argsme'

if __name__ == '__main__':
    sqliteConnection = sqlite3.connect('../../sql.db')
    cursor = sqliteConnection.cursor()
    insert_query = 'INSERT INTO arguments(doc_id, title, description, conclusion) VALUES (?,?,?,?)'
    for i in range(DOCS_COUNT):
        file_path = f'{DOCS_PATH}/argsme_obj_{i}.json'
        argument = json_to_argument(file_path)
        cursor.execute(insert_query, (argument.doc_id, argument.title, argument.description, argument.conclusion))
        print(f'raw {i} inserted')
    sqliteConnection.commit()
    cursor.close()
