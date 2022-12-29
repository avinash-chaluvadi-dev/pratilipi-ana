from typing import Union

from app.core import constants, exceptions
from app.ml.text_normalization.preprocess import txt_normalize


def text_normalization(transcript: Union[str, list]) -> Union[str, list]:
    """
    Text Normalization for a speech to text output
       :param transcript : Loads the input sentence from json
       :return : A list a text normalization in a dict format.

    """
    if not isinstance(transcript, (list, str)):
        raise exceptions.BadRequestException(
            constants.NORMALIZATION_LIST_STRING_EXCEPTION
        )

    elif isinstance(transcript, str):
        final_transcripts = []
        result = txt_normalize(transcript)
        final_transcripts.append({"transcript": transcript, "text_normalize": result})
        return final_transcripts
    else:
        final_transcripts = []
        for i in transcript:
            output = txt_normalize(i)
            final_transcripts.append({"transcript": i, "text_normalize": output})
        return final_transcripts
