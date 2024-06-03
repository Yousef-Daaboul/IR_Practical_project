import xml.etree.ElementTree as eT

from clinical_trial import ClinicalTrial


def xml_to_clinical_trial(file_name: str) -> ClinicalTrial:
    tree = eT.parse(file_name)
    doc_id = tree.find('id_info').find('nct_id').text
    title = tree.find('brief_title').text
    description_element = tree.find('detailed_description')
    if description_element:
        description = description_element.find('textblock').text
    else:
        description = tree.find('eligibility').find('criteria').find('textblock').text
    summary = tree.find('brief_summary').find('textblock').text
    return ClinicalTrial(doc_id, title, description, summary)
