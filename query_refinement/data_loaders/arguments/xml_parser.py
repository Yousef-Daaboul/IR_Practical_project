import xml.etree.ElementTree as eT
from typing import List

from query_refinement.data_loaders.arguments.argument_query import ArgumentQuery


def xml_to_argument_query(file_path: str) -> List[ArgumentQuery]:
    tree = eT.parse(file_path)
    root = tree.getroot()

    topics = []

    for topic in root.findall('topic'):
        number = topic.find('number').text
        title = topic.find('title').text
        description = topic.find('description').text
        narrative = topic.find('narrative').text
        argument_query = ArgumentQuery(number, title, description, narrative)

        topics.append(argument_query)

    return topics
