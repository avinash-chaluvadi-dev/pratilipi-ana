""" [Preprocessing module for Topic classifier]

This module holds all the custom pre-processing functions required for 
TOPIC_CLASSIFIER package

This file can also be imported as a module and contains the following
functions:

    * process_label_data      - encodes the output column and returns encoded list of labels/topics
    * general_substitutions   - replaces the words with common substitutions
    * clean_sentence          - cleans the sentence by removing unncessary patterns of words, 
                                stopwords etc and returns cleaned version of sentence
                                     type of object is neither list nor string
    * preprocess_data         - returns the processed version of input and output which then topic_classifier 
                                consumes to train/serve
"""

import re
import string
import warnings

import numpy as np

from app.ml.topic_classifier import config
from app.ml.topic_classifier.utils import utils_tools


def process_label_data(label: list) -> list:

    """
    This function encodes each entry/label in list into a one-hot
    encoded list of shape (1,16) because each sentence can have more
    than one label

    Parameters
    ----------
        :param label (list): Label list which is to be encoded

    Returns
    -------
        :processed_label (list): Encoded list of labels/topics

    """

    processed_label = []
    label_split_pattern = re.compile(
        r"\s*[;#]+\s*"
    )  # Split pattern to split the output label string
    for index, _label in enumerate(label):
        encoded_label = [0] * len(
            config.LABELS
        )  # Let's create a list of zeroes with length of 16
        for word in re.split(label_split_pattern, _label):
            encoded_label[
                config.LABELS.index(word)
            ] += 1  # Modifying the list according to index of labels defined in config.py
        processed_label.append(encoded_label)
    return np.array(processed_label)


def general_substitutions(sentence: str) -> str:

    """
    This function cleans the input sentence by substituing the
    words with defined pattern of words

    Parameters
    ----------
        :param sentence (str): Input sentence which has to be cleaned

    Returns
    -------
        :sentence (str): Processed version of sentence

    """

    substitution_patterns = [
        (r"\n", " "),
        (r"\s+", " "),
        (r"\s*\.+", " "),
        (r"\'m", "am"),
        (r"\'s", "is"),
        (r"\'re", "are"),
        (r"n\'t", "not"),
        (r"\'ll", "will"),
        (r"LAUSD", " "),
        (r"mbr", "member"),
        (r"Repeat caller", " "),
        (r"appt", "appointment"),
    ]

    ## Substitutes the words if it matches with defined patterns with actal words present in substitution_patterns tuple
    for old, new in substitution_patterns:
        sentence = re.sub(old, new, sentence, flags=re.I)
    return sentence


# Helper function for removing the unwanted words from sentence
def clean_sentence(sentence: str) -> str:

    """
    This function cleans the input sentence by removing/substituting
    the words matched with the defined patterns

    Parameters
    ----------
        :param sentence (str): Input sentence which has to be cleaned

    Returns
    -------
        :sentence (str): Processed version of sentence

    """

    unwanted_pattern = re.compile(
        r"([-:@#$/]+)|([*(\[]+.*?[*)\]]+)", flags=re.I
    )  # pattern for removal of unwanted words, punctuations, symbols, brackets etc from sentence

    email_pattern = re.compile(
        r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", flags=re.I
    )  # pattern for removal of emails from sentence

    id_pattern = re.compile(
        r"([0-9]+[a-zA-Z]+[0-9a-zA-Z]+)|([A-Z]+[0-9]+[A-Z]+)", flags=re.I
    )  # pattern for removal of member_id's, phone numbers, callback_id's from sentence

    month_pattern = re.compile(
        r"((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Sept|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?))",
        flags=re.I,
    )  # pattern for removal of month names from sentence

    ## Substitutes words if matches with above patterns
    sentence = re.sub(unwanted_pattern, " ", sentence)
    sentence = re.sub(email_pattern, " ", sentence)
    sentence = re.sub(id_pattern, " ", sentence)
    sentence = re.sub(month_pattern, " ", sentence)
    sentence = re.sub(r"\d+", " ", sentence)
    sentence = general_substitutions(sentence=sentence)
    return sentence.lower()


def preprocess_data(message: list, label: list = None, mode="train") -> dict:
    """
    This function is the entrypoint for text pre-procesing and it cleans,
    processes the input and output in format required for topic_classifier

    Parameters
    ----------
        :param message (list): Message list which is to be processed/cleaned
        :param label (list): Label list which is to be processed/cleaned
        :param mode (str): Mode can be train/eval/serve

    Returns
    -------
        :processed_dict (dict): Processed dictionary of messages, and labels

    """

    stop_words = (
        utils_tools.get_stop_words()
    )  # Initializes the stopwords from nltk package

    punctuations = list(
        string.punctuation
    )  # Initializes the punctuations from string package

    ## Processing is different for training and serving, because training data requires output processing as well
    if mode == "train":
        for index, (sentence, _label) in enumerate(zip(message, label)):
            cleaned_sentence = clean_sentence(
                sentence=sentence
            )  # Calling the clean_sentence for cleaning and removal of unwanted words
            if len(sentence) <= 1:  # Removes the sentences with one/two words
                message.pop(index)
                label.pop(index)
            elif len(sentence) > 1:
                message[index] = " ".join(
                    [
                        word
                        for word in cleaned_sentence.split()
                        if word not in stop_words
                        if word not in punctuations
                    ]
                )  # Updates the message list after removing stopwords and punctuations
                label[index] = _label.strip()

        ## Zipping the message and lable and transforming into list
        data = list(map(list, zip(*list(set(zip(message, label))))))
        message = np.array(data[0])  # List of cleaned/processed messages
        label = np.array(data[1])

        ## Calling the process_label_data to process the output list
        processed_label = np.array(
            process_label_data(label=data[1])
        )  # List of cleaned/processed output labels
        return {"message": message, "label": label, "processed_label": processed_label}

    elif mode in ["eval", "serve"]:
        for index, sentence in enumerate(message):
            cleaned_sentence = clean_sentence(
                sentence=sentence
            )  # Calling the clean_sentence for cleaning and removal of unwanted words
            message[index] = " ".join(
                [
                    word
                    for word in cleaned_sentence.split()
                    if word not in stop_words
                    if word not in punctuations
                ]
            )  # Updates the message list after removing stopwords and punctuations
        return {"message": message}
