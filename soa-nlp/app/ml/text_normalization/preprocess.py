import string

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def remove_punct(tranascript):
    """
    Remove punctuations from a given transcript
    input : sentence string.
    output : processed string.
    """
    puct_to_remove = string.punctuation.replace(".", "")
    puct_to_remove1 = puct_to_remove.replace("(", "")
    puct_to_remove2 = puct_to_remove1.replace(")", "")
    res = [i for i in tranascript if i not in puct_to_remove2]
    res = "".join(res)
    return res


def wordtokenize(transcript):
    """
    Text Tokenization
    input : sentence string.
    output : List of tokens for a gives string.
    """
    tokens = word_tokenize(transcript)
    return tokens


def apply_lemmatization(tokens, wnl=WordNetLemmatizer()):
    """
    Applying lemmatization to a sentence
    input : sentence string.
    output : processed string.
    """
    return [wnl.lemmatize(token) for token in tokens]


def txt_normalize(transcript):
    """
    Applying basic cleaning to the text
    input : sentence string.
    output : processed string.
    """
    rem_punct = remove_punct(transcript)
    tokenization = wordtokenize(rem_punct)
    lemmatization = apply_lemmatization(tokenization)
    text = " ".join([token for token in lemmatization])
    text = text.replace("( ","(")
    text = text.replace(" )",")")
    text = text.replace(" .",".")
    return text
