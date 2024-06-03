import os
import sqlite3
import glob

from query_refinement.data_loaders.clinical.xml_parser import xml_to_clinical_query


def process_file():
    xml_path = '../../data_source/clinical_queries.xml'
    try:
        clinical_queries = xml_to_clinical_query(xml_path)

        for query in clinical_queries:
            cursor.execute(insert_query, (
                query.query_id, query.disease, query.gene, query.demographic, query.other))
    except Exception as e:
        print(f"Error processing file: {e}")


if __name__ == '__main__':
    sqliteConnection = sqlite3.connect('../queries.db')
    cursor = sqliteConnection.cursor()
    insert_query = 'INSERT INTO clinical_queries(query_id, disease, gene, demographic,other) VALUES (?,?,?,?,?)'
    process_file()
    sqliteConnection.commit()
    cursor.close()
