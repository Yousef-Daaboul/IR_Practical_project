import os
import sqlite3
from xml_parser import xml_to_clinical_trial
import glob

DOCS_PATH = '/home/nezar/Desktop/datasets/clinical_trial/clinicaltrials_xml'


def process_file():
    for i in range(32):
        for j in range(100):
            current_file = f'{i:03d}/{i:03d}{j:02d}'
            current_path = f'{DOCS_PATH}/{current_file}'
            xml_files = glob.glob(os.path.join(current_path, "*.xml"))
            for xml_file in xml_files:
                print(xml_file)
                try:
                    clinical_trial = xml_to_clinical_trial(xml_file)
                    cursor.execute(insert_query, (
                        clinical_trial.doc_id, clinical_trial.title, clinical_trial.description,
                        clinical_trial.summary))
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    sqliteConnection = sqlite3.connect('../../sql.db')
    cursor = sqliteConnection.cursor()
    insert_query = 'INSERT INTO clinical_trials(doc_id, title, description, summary) VALUES (?,?,?,?)'
    process_file()
    sqliteConnection.commit()
    cursor.close()
