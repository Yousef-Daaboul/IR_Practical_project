from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet

from services.query_refinement.auto_complete import process_text


def expand_query(query, with_text_process: bool = True):
    if with_text_process:
        query = process_text(query, True)

    tokens = word_tokenize(query)
    tagged_tokens = pos_tag(tokens)

    expanded_query = []
    for word, tag in tagged_tokens:
        wn_tag = get_wordnet_pos(tag)
        if wn_tag:  # If the word has a corresponding WordNet POS tag
            synonyms = get_synonyms(word, wn_tag)
            if synonyms:
                expanded_query.extend(synonyms)
            else:
                expanded_query.append(word)
        else:
            expanded_query.append(word)  # Keep the original word if no POS tag match

    return {"expanded_query": ' '.join(expanded_query)}


def get_synonyms(word, pos):
    synonyms = set()
    for syn in wordnet.synsets(word, pos):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return synonyms


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None
