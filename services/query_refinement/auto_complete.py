import requests
from constants import ServicesNames, success_num
from services.query_refinement.query_complete.match_logs import fetch_similar_queries
from services.query_refinement.query_complete.match_queries import match_queries
from services.query_refinement.query_complete.match_titles import match_titles
from services.registry_client import get_service


def query_complete(query, dataset_id, with_correct_spelling, max_results=10):
    cleaned_text = process_text(query, with_correct_spelling)

    print(f'Cleaned text: {cleaned_text}')

    similar_queries = fetch_similar_queries(cleaned_text, success_num, dataset_id)
    similar_queries = format_similar_queries_results(similar_queries)
    print(f'similar_queries : {similar_queries}')

    complete_queries = match_queries(cleaned_text, dataset_id)
    complete_queries = format_query_results(complete_queries, dataset_id)
    print(f'complete queries: {complete_queries}')

    complete_titles = match_titles(cleaned_text, dataset_id)
    complete_titles = format_titles_results(complete_titles)
    print(f'complete_titles: {complete_titles}')

    results = combine_results(similar_queries, complete_queries, complete_titles, max_results)

    print(f'results: {results}')

    return results


def format_query_results(results, dataset_id):
    formatted_results = []
    for result in results:
        if dataset_id == 1:
            formatted_str = f"disease: {result['disease']}, gene: {result['gene']}, demographic: {result['demographic']}"
            if result['other'] != 'None' and result['other']:
                formatted_str += f", other: {result['other']}"
        else:
            formatted_str = f"{result['title']} {result['description']} {result['narrative']}"

        formatted_results.append(formatted_str)
    return formatted_results


def format_similar_queries_results(results):
    formatted_results = []
    for result in results:
        formatted_results.append(result[1])

    return formatted_results


def format_titles_results(results):
    formatted_results = []
    for result in results:
        formatted_results.append(result["title"])

    return formatted_results


def combine_results(similar_queries, complete_queries, complete_titles, max_results):
    result = []

    # Take up to 2 elements from similar_queries
    result.extend(similar_queries[:2])
    remaining_slots = max_results - len(result)

    # Take up to 4 elements from complete_queries
    num_complete_queries = min(len(complete_queries), 4)
    result.extend(complete_queries[:num_complete_queries])
    remaining_slots -= num_complete_queries

    # Take up to 4 elements from complete_titles
    num_complete_titles = min(len(complete_titles), 4)
    result.extend(complete_titles[:num_complete_titles])
    remaining_slots -= num_complete_titles

    # If there's any remaining slots, fill them with elements from the other arrays
    if remaining_slots > 0:
        remaining_complete_queries = complete_queries[num_complete_queries:]
        remaining_complete_titles = complete_titles[num_complete_titles:]

        # Fill remaining slots from remaining_complete_queries
        result.extend(remaining_complete_queries[:remaining_slots])
        remaining_slots -= len(remaining_complete_queries[:remaining_slots])

        # If there's still remaining slots, fill them with remaining_complete_titles
        if remaining_slots > 0:
            result.extend(remaining_complete_titles[:remaining_slots])

    return result[:max_results]


def process_text(text: str, with_correct_spelling: bool = False) -> str:
    url = get_service(ServicesNames.text_processing)
    params = {'enable_spell_checking': with_correct_spelling}
    data = {
        'text': text,
    }
    result = requests.post(url=url, json=data, params=params)
    return result.json()['result']
