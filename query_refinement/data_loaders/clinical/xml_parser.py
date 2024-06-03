import xml.etree.ElementTree as eT
from typing import List

from query_refinement.data_loaders.clinical.clinical_query import ClinicalQuery


def xml_to_clinical_query(file_path: str) -> List[ClinicalQuery]:
    tree = eT.parse(file_path)
    root = tree.getroot()

    topics = []

    for topic in root.findall('topic'):
        number = topic.get('number')
        disease = topic.find('disease').text
        gene = topic.find('gene').text
        demographic = topic.find('demographic').text
        other = topic.find('other').text

        clinical_query = ClinicalQuery(number, disease, gene, demographic, other)
        topics.append(clinical_query)

    return topics

