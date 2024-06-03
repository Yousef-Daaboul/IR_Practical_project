import json

from argument import Argument


def json_to_argument(file_name: str) -> Argument:
    with open(file_name, "rb") as file:
        tree = json.load(file)
        doc_id = tree['id']
        title = tree['context']['discussionTitle']
        description = tree['context']['sourceText']
        conclusion = tree['conclusion']
    file.close()
    return Argument(doc_id, title, description, conclusion)
