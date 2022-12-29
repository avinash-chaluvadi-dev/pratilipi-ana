from typing import Optional, Union

from pydantic import BaseModel, StrictStr


class CognitiveBase(BaseModel):
    transcript: Union[StrictStr, list]


class EntityPrediction(BaseModel):
    entity: str
    label: str
    start: int
    end: int


class NerPrediction(BaseModel):
    transcript: str
    Ner: list[EntityPrediction]


class ClassifierPrediction(BaseModel):
    transcript: str
    label: list
    confidence_score: list


class TextNormalization(BaseModel):
    transcript: str
    text_normalize: str


class NerResponse(BaseModel):
    predictions: list[NerPrediction]


class ClassifierResponse(BaseModel):
    predictions: list[ClassifierPrediction]


class NormalizationResponse(BaseModel):
    predictions: list[TextNormalization]
