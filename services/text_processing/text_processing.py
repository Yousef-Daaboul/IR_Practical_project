import string
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from typing import List
from spellchecker import SpellChecker


def remove_punctuation_tokenizer(txt: str):
    """Removes punctuation from a string.

    Args:
        txt: The string to remove punctuation from.

    Returns:
        A list of words with punctuation removed.
    """
    # print('Start remove_punctuation')
    new_tokens = []
    txt = txt.lower()
    for token in txt.split():
        new_tokens.append(token.translate(str.maketrans('', '', string.punctuation)))
    # print('Finish remove_punctuation')
    return new_tokens


def remove_stopwords(tokens: List[str]) -> List[str]:
    # print('Start remove_stopwords')
    filtered = []
    for word in tokens:
        if word not in stopwords.words('english'):
            filtered.append(word)
    # print('Finish remove_stopwords')
    return filtered


def correct_sentence_spelling(tokens: List[str]) -> List[str]:
    # print('Start correct_sentence_spelling')
    spell = SpellChecker()
    c = 0
    misspelled = spell.unknown(tokens)
    for i, token in enumerate(tokens):
        if token in misspelled:
            corrected = spell.correction(token)
            if corrected is not None:
                c += 1
                tokens[i] = corrected
    # print(f'Finish correct_sentence_spelling : {c} words corrected')
    return tokens


def get_wordnet_pos(tag_parameter):
    tag = tag_parameter[0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def lemmatization(tokens: List[str]) -> List[str]:
    # print('Start lemmatization')
    pos_tags = pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag)) for word, tag in pos_tags]
    # print('Finish lemmatization')
    return lemmatized_words


def text_processor(txt: str, enable_spell_checking=False):
    tokens = remove_punctuation_tokenizer(txt)
    tokens = remove_stopwords(tokens)
    if enable_spell_checking:
        tokens = correct_sentence_spelling(tokens)
    tokens = lemmatization(tokens)
    return " ".join(tokens)
