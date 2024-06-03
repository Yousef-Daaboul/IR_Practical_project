import os
import pickle
import pprint

import requests
import csv

from dotenv import load_dotenv

from constants import clinical_trials_queries_file, clinical_trials_qrels_file, ServicesNames, load_pickle_file, \
    clinical_trials_queries_file

load_dotenv()


def get_query_results(use_cache=False):
    if use_cache:
        return load_pickle_file(clinical_trials_queries_file)
    results = {}
    base_url = os.getenv('BASE_URL')
    port = os.getenv('MATCHING_PORT')
    url = f'{base_url}:{port}/{ServicesNames.matching}'
    with (open('queries.csv', 'r') as csvfile):
        reader = csv.reader(csvfile)
        for query_id, query in reader:
            if int(query_id) == 10:
                pass
            result = requests.get(f'{url}/1?query={query}')
            docs_ids = [item['doc_id'] for item in result.json()]
            results[int(query_id)] = docs_ids
        csvfile.close()
    print(results)
    with open(clinical_trials_queries_file, "wb") as f:
        pickle.dump(results, f)


def get_qrels(use_cache=False):
    if use_cache:
        return load_pickle_file(clinical_trials_qrels_file)
    qrels_dict = {}
    with (open('qrels.csv', 'r') as csvfile):
        reader = csv.reader(csvfile)
        for qid, doc_id, rel, _ in reader:
            int_rel = int(rel)
            int_qid = int(qid)
            if int_qid not in qrels_dict:
                qrels_dict[int_qid] = []
            if int_rel > 0:
                qrels_dict[int_qid].append({'doc_id': doc_id, 'rel': int_rel})
        csvfile.close()
    pprint.pprint(qrels_dict)
    print(len(qrels_dict))
    with open(clinical_trials_qrels_file, "wb") as f:
        pickle.dump(qrels_dict, f)


if __name__ == '__main__':
    get_query_results()
    # get_qrels()
