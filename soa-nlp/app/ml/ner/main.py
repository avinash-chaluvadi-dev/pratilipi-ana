import re
from typing import Union

import spacy
from spacy.language import Language

from app.core import constants, exceptions
from app.ml.ner import config


@Language.component("remove_entities_except_person")
def remove_entities_except_person(input_sentence: Language) -> Language:
    """
    Add New rule in spacy ner pipeline which consist only PERSON
        :param input_sentence : Loads the input sentence from a list
        :return : input_sentence

    """
    ents = list(input_sentence.ents)
    for ent in ents[:]:
        if ent.label_ != "PERSON":
            ents.remove(ent)
    ents = tuple(ents)
    input_sentence.ents = ents
    return input_sentence


Language.component("remove_entities_except_person", func=remove_entities_except_person)


def spacy_ner(
    input_sentence: Union[str, list], expressions: dict = None
) -> Union[list, str]:
    """
    Predict entities from a input sentence
        :param expressions:
        :param input_sentence : Loads the input sentence from json
        :return : A list of Entity name, Label Name, start and end indexes

    """
    if not isinstance(input_sentence, (list, str)):
        raise exceptions.BadRequestException(constants.NER_LIST_STRING_EXCEPTION)

    elif isinstance(input_sentence, str):
        if not expressions:
            expressions = config.regex_expression
        spans = []
        final_result = []
        unit = {}
        result = []
        ner_rule = spacy.load(config.spacy_model)
        ner_rule.add_pipe("remove_entities_except_person")
        doc = ner_rule(input_sentence)
        unit["transcript"] = input_sentence
        for label, expression in expressions.items():
            for match in re.finditer(expression, input_sentence):
                start, end = match.span()
                entity = doc.char_span(start, end, label=label)
                if entity:
                    spans.append(entity)
        entities = list(doc.ents)
        entities = entities + spans
        entities = tuple(entities)
        for ent in entities:
            result.append(
                {
                    "entity": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                }
            )
        unit["Ner"] = result
        final_result.append(unit)
        return final_result
    else:
        if not expressions:
            expressions = config.regex_expression
        final_result = []
        ner_rule = spacy.load(config.spacy_model)
        ner_rule.add_pipe("remove_entities_except_person")
        for transcript in input_sentence:
            doc = ner_rule(transcript)
            unit = {}
            spans = []
            unit["transcript"] = transcript
            for label, expression in expressions.items():
                for match in re.finditer(expression, transcript):
                    start, end = match.span()
                    entity = doc.char_span(start, end, label=label)
                    if entity:
                        spans.append(entity)
            entities = list(doc.ents)
            entities = entities + spans
            entities = tuple(entities)
            result = []
            for ent in entities:
                result.append(
                    {
                        "entity": ent.text,
                        "label": ent.label_,
                        "start": ent.start_char,
                        "end": ent.end_char,
                    }
                )
            unit["Ner"] = result
            final_result.append(unit)
        return final_result
