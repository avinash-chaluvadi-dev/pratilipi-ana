import pickle

import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer

from app.core.exceptions import BadRequestException
from app.ml.classifier_rule import config
from app.ml.classifier_rule.utils.data_preprocessing import clean_text

transformer = TfidfTransformer()
loaded_vec = TfidfVectorizer(
    decode_error="replace", vocabulary=pickle.load(open(config.vocab, "rb"))
)
corex_model = pickle.load(open(config.model, "rb"))


def prediction_on_one_sen(sentence_clean, categories):
    """

    :param sentence_clean: cleaned text
    :param categories: categories for classification
    :return: label after classification
    """
    tfidf = transformer.fit_transform(
        loaded_vec.fit_transform(np.array([sentence_clean]))
    ).astype(float)
    predictions_test = corex_model.predict_proba(tfidf)

    if np.min(predictions_test[0][0]) == np.max(predictions_test[0][0]):

        return categories[-1]
    else:
        index_max = np.argmax(predictions_test[0][0])
        return categories[index_max]


def classifier_rule(sentence):
    """
    This Module Runs the predictions of topic model COREX for a given input sentence.
    - Converts the input sentences into TFIDF Vector required for predictions
    - Corex prediction on the TFIDF Vector
        :param sentence: consume aws transctibe output as a input for classifier model as a string
        :return list of dictonary:
                                 transcript: Input raw text (string)
                                 Label: Predicted Label (string)
                                 confidence score: [] (empty list)
    """
    res_lis = []
    categories = config.categories
    if not isinstance(sentence, (list, str)):
        raise BadRequestException()

    elif isinstance(sentence, str):

        res = {}
        res["transcript"] = sentence
        res["label"] = []
        res["confidence_score"] = []
        sentence_clean = clean_text(sentence)
        res["label"].append(prediction_on_one_sen(sentence_clean, categories))
        res_lis.append(res)
        return res_lis
    else:
        for each_sen in sentence:
            res = {}
            res["transcript"] = each_sen
            res["label"] = []
            res["confidence_score"] = []
            sentence_clean = clean_text(each_sen)
            res["label"].append(prediction_on_one_sen(sentence_clean, categories))
            res_lis.append(res)
        return res_lis
