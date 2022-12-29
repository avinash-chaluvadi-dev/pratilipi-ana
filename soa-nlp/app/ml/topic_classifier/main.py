""" [Topic Classifier]

This module allows the user to classify the sentence into zero or 
mutually non-exclusive class labels defined in "config.py"

This script requires packages mentioned in "requirements.txt "to 
be installed within the Python environment you are running this script in

This file can also be imported as a module and contains the following
functions:

    * topic_classifier - returns output labels and confidence scores.
"""
import logging
from typing import Union

from app.core import constants, exceptions
from app.ml.topic_classifier import config
from app.ml.topic_classifier.utils import preprocess, utils_tools

logger = logging.getLogger(__name__)


def topic_classifier(message: Union[str, list]) -> Union[list, str]:
    """
    This function handles preprocessing, cleaning and classification
    of each sentence into zero or more mutually non-exclusive class labels
    and returns list of dictionaries

    Parameters
    ----------
        :param message (list or str): The Message or voicemail which is to be classified

    Returns
    -------
        :hypothesis (list): List of dictionary objects with input messages, output labels and confidence scores

    Raises
    ------
        TypeError:  When input message parameter is neither list nor string
        ValueError: When input message parameter is None
    """

    if not isinstance(message, (list, str)):
        logger.error("Invalid instance for transcript")
        raise exceptions.BadRequestException(
            constants.TOPIC_CLASSIFIER_LIST_STRING_EXCEPTION
        )

    elif isinstance(message, str):
        logger.debug("Received single transcript for prediction")
        classifier = utils_tools.load_model(
            model_name=config.MODEL_NAME
        )  # Loads the model from mounted file system in form of bytes
        logger.info(f"model {config.MODEL_NAME} loaded")

        cleaned_message = preprocess.preprocess_data(
            message=[message], mode="serve"
        ).get(
            "message"
        )  # Let's do pre-processing before feeding it into model

        encoded_message = utils_tools.sentence_embeddings(
            message=cleaned_message
        )  # Encodes the message/sentence in the form of vectors/embeddings

        sparse_hypothesis = classifier.predict(
            encoded_message
        )  # Predicts the labels/topics for input message
        sparse_probabilities = classifier.predict_proba(
            encoded_message
        )  # Predicts the probability/confidence_score for each input message

        hypothesis = utils_tools.decode_labels(
            sparse_hypothesis
        )  # Decodes the labels into actual labels

        topic_classifier_output = utils_tools.create_response(
            message=[message],
            hypothesis=hypothesis,
            probabilities=sparse_probabilities,
        )  # Combines the transcript, predicted label and confidence_score dictionaries into a list

        return topic_classifier_output

    else:
        logger.debug("Received list of transcripts for prediction")
        classifier = utils_tools.load_model(
            model_name=config.MODEL_NAME
        )  # Loads the model from mounted file system in form of bytes
        logger.info(f"model {config.MODEL_NAME} loaded")

        cleaned_message = preprocess.preprocess_data(message=message, mode="serve").get(
            "message"
        )  # Let's do pre-processing before feeding it into model

        encoded_message = utils_tools.sentence_embeddings(
            message=cleaned_message
        )  # Encodes the message/sentence in the form of vectors/embeddings

        sparse_hypothesis = classifier.predict(
            encoded_message
        )  # Predicts the labels/topics for input message

        sparse_probabilities = classifier.predict_proba(
            encoded_message
        )  # Predicts the probability/confidence_score for each input message

        hypothesis = utils_tools.decode_labels(
            sparse_hypothesis
        )  # Decodes the labels into actual labels

        topic_classifier_output = utils_tools.create_response(
            message=message,
            hypothesis=hypothesis,
            probabilities=sparse_probabilities,
        )  # Combines the transcript, predicted label and confidence_score dictionaries into a list
        return topic_classifier_output
