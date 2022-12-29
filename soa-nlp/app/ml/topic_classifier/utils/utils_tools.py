""" [Utility module for Topic classifier]

This module holds all the general purpose utility functions 
required for TOPIC_CLASSIFIER package

This file can also be imported as a module and contains the following
functions:

    * get_stop_words          - returns the stopwords from nltk if present otherwise it downloads 
                                and then returns stopwords
    * sentence_embeddings     - encodes the input column and returns encoded list of messages/sentences
    * load_model              - loads the model from any mounted file system in form of bytes and returns
                                     type of object is neither list nor string
    * decode_labels           - returns the actual labels defined in "config.py" from one-hot-encoded list
"""

import os
import pickle

import nltk
import numpy as np

from app.ml.topic_classifier import config
from app.ml.topic_classifier.utils import preprocess


def get_stop_words() -> list:
    """
    This function retruns stopwords in the form of list if present on
    nltk_data path, otherwise it downloads and then returns

    Returns
    -------
        :stop_words (list): List of of stop_words aka most common and repetitive words

    Raises
    ------
        LookupError:  When nltk cannont find the stopwords on any of the
                      nltk_data paths
    """

    try:
        stop_words = nltk.corpus.stopwords.words(
            "english"
        )  # Loads the stopwords from any of the nltk_data list of paths
        return stop_words

    except LookupError:
        stop_words = nltk.download(
            "stopwords"
        )  # Let's download the stopwords and append the path to nltk_data
        if stop_words:
            stop_words = nltk.corpus.stopwords.words(
                "english"
            )  # Loads the stopwords from any of the nltk_data list of paths
            return stop_words


def sentence_embeddings(message: list) -> list:

    """
    This function retruns the sentence embeddings for each sentence/message in the list

    Parameters
    ----------
        :param message (list): The Message or voicemail which is to be encoded

    Returns
    -------
        :encoded_message (list): Encoded list of messages/sentences in form of vectors/embeddings
    """

    return config.model.encode_sentences(
        message, combine_strategy="mean"
    )  # Loads and encodes all the sentences present in list


def load_model(model_name: str):

    """
    This function can load the model from any mounted file system and
    returns the model in form of bytes

    Parameters
    ----------
        :param model_name (str): Name of the model which is to be returned

    Returns
    -------
        :model : Multi Label topic_classifier object for predictions
    """

    model_path = os.path.join(config.MODEL_DIR, model_name)  # Path of model to load
    with open(model_path, "rb") as f:
        model = pickle.load(f)
        return model


def decode_labels(hypothesis: list) -> list:

    """
    This function transforms model predictions into actual labels defined in "config.py"

    Parameters
    ----------
        :param hypothesis (list): Model Predictions which are to be transformed

    Returns
    -------
        :final_predictions (list) : Transformed outputs/labels in form of 2D List
    """

    final_predictions = []
    for prediction in hypothesis:
        label = []
        for index, encoded_label in enumerate(
            prediction.A[0]
        ):  # Let's access the list of predictions from lil sparse matrix
            if encoded_label == 1:
                label.append(
                    str(config.LABELS[index])
                )  # Get's the actual label from config.py and appends into final_predictions
        final_predictions.append(label)
    return final_predictions


def create_response(message: list, hypothesis: list, probabilities: list) -> list:

    """
    This function creates the reponse by combining model predictions,
    message/transcript and confidence_score into a dictionary for each
    meesage/transcript

    Parameters
    ----------
        :param message (list): Input Messages which will get attached to response
        :param hypothesis (list): Decoded labels which will get attached to response
        :param probabilities(sparse.lil_matrix): sparse matrix of probabilities which will get attached to reponse
    Returns
    -------
        :topic_classifier_output (list) : Trnaformed and combined topic classifier output
    """

    topic_classifier_output = []
    for _message, _hypothesis, probability in zip(message, hypothesis, probabilities):
        processed_message = preprocess.general_substitutions(sentence=_message)
        response_dict = dict()
        if probability.shape[0] > 1:
            response_dict["transcript"] = processed_message
            response_dict["label"] = _hypothesis
            response_dict["confidence_score"] = list(np.amax(probability.A[0], axis=1))
            topic_classifier_output.append(response_dict)
        else:
            response_dict["transcript"] = processed_message
            response_dict["label"] = _hypothesis
            response_dict["confidence_score"] = [np.amax(probability.A[0])]
            topic_classifier_output.append(response_dict)

    return topic_classifier_output
