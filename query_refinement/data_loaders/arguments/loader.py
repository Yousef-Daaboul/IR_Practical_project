import os
import sqlite3
import glob

from query_refinement.data_loaders.arguments.xml_parser import xml_to_argument_query


def process_file():
    xml_path = '../../data_source/arguments_queries.xml'
    try:
        argument_queries = xml_to_argument_query(xml_path)

        for query in argument_queries:
            cursor.execute(insert_query, (
                query.query_id, query.title, query.description, query.narrative))
    except Exception as e:
        print(f"Error processing file: {e}")


if __name__ == '__main__':
    sqliteConnection = sqlite3.connect('../queries.db')
    cursor = sqliteConnection.cursor()
    insert_query = 'INSERT INTO arguments_queries(query_id, title, description, narrative) VALUES (?,?,?,?)'
    process_file()
    sqliteConnection.commit()
    cursor.close()
