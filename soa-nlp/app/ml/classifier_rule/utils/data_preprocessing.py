import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = stopwords.words("english")
stop_words_to_keep = ["not", "no"]
stop_words = list(set(stop_words) - set(stop_words_to_keep))


def tokenize_text(book_text):
    """
    Text Tokenization
    input : sentence string
    output : processed string
    """
    TOKEN_PATTERN = r"\s+"
    regex_wt = nltk.RegexpTokenizer(pattern=TOKEN_PATTERN, gaps=True)
    word_tokens = regex_wt.tokenize(book_text)
    return word_tokens


def remove_characters_after_tokenization(tokens):
    """
    Removing characters like single quotes from an sentence
    input : sentence string
    output : processed string
    """
    pattern = re.compile("[{}]".format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub("", token) for token in tokens])
    return filtered_tokens


def remove_stopwords(tokens):
    """
    removing stop words from a sentence
    input : sentence string
    output : processed string
    """

    filtered_tokens = [token for token in tokens if token not in stop_words]
    return filtered_tokens


def apply_lemmatization(tokens, wnl=WordNetLemmatizer()):
    """
    Applying lemmatization to a sentence
    input : sentence string
    output : processed string
    """
    return [wnl.lemmatize(token) for token in tokens]


def clean_text(text):
    """
    Applying basic cleaning to the text
    input : sentence string
    output : processed string
    """
    text = text.lower()
    tokens = tokenize_text(text)
    tokens = remove_characters_after_tokenization(tokens)

    tokens = remove_stopwords(tokens)
    tokens = apply_lemmatization(tokens)
    text = " ".join([token for token in tokens])
    return text
