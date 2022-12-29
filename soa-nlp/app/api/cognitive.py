from fastapi import APIRouter

from app.ml.classifier_rule.main import classifier_rule
from app.ml.ner.main import spacy_ner
from app.ml.text_normalization.main import text_normalization
from app.ml.topic_classifier.main import topic_classifier
from app.schemas import cognitive
from app.schemas.cognitive import (ClassifierResponse, NerResponse,
                                   NormalizationResponse)

v1_router = APIRouter(prefix="/cognitive", tags=["cognitive"])


@v1_router.post("/ner", response_model=cognitive.NerResponse)
async def ner(payload: cognitive.CognitiveBase):
    predictions = spacy_ner(payload.transcript)
    return NerResponse(predictions=predictions)


@v1_router.post("/classifier_model", response_model=ClassifierResponse)
async def topic_classifier_model(payload: cognitive.CognitiveBase):
    predictions = topic_classifier(message=payload.transcript)
    return ClassifierResponse(predictions=predictions)


@v1_router.post("/classifier_rule", response_model=ClassifierResponse)
async def topic_classifier_rule(payload: cognitive.CognitiveBase):
    predictions = classifier_rule(payload.transcript)
    return ClassifierResponse(predictions=predictions)


@v1_router.post("/text_normalization", response_model=NormalizationResponse)
async def text_normalize(payload: cognitive.CognitiveBase):
    predictions = text_normalization(payload.transcript)
    return NormalizationResponse(predictions=predictions)
