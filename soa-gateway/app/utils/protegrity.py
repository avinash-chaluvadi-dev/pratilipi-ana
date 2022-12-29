import requests
import json
from app.core.config import settings
from app.core.constants import PROTEGRITY_HEADERS
from app.core.exceptions import (
    UnauthorisedError,
    ForbiddenException,
    NotAcceptableError,
    RequestTimeoutError,
)


class ProtegrityConfigurationUtils:
    def __init__(self, data):
        self.headers = PROTEGRITY_HEADERS
        self.username = settings.PROTEGRITY_USERNAME
        self.password = settings.PROTEGRITY_PASSWORD
        self.protect_url = settings.TOKENIZE_URL_JSON
        self.unprotect_url = settings.DETOKENIZE_URL_JSON
        self.data = data
        self.base_certificate_status = settings.BASE_CERTIFICATE
        self.exceptions = {
            401: UnauthorisedError,
            403: ForbiddenException,
            406: NotAcceptableError,
            408: RequestTimeoutError,
        }

    def tokenization(self):

        payload = json.dumps(self.data)

        tokenize_response = requests.request(
            "POST",
            self.protect_url,
            auth=(self.username, self.password),
            headers=self.headers,
            data=payload,
            verify=self.base_certificate_status,
            timeout=settings.DEFAULT_TIMEOUT,
        )

        if tokenize_response.status_code in self.exceptions:
            raise self.exceptions[tokenize_response.status_code]

        return tokenize_response.json()

    def detokenization(self):
        payload = str(json.dumps(self.data))

        detokenize_response = requests.request(
            "POST",
            self.unprotect_url,
            auth=(self.username, self.password),
            headers=self.headers,
            data=payload,
            verify=self.base_certificate_status,
            timeout=settings.DEFAULT_TIMEOUT,
        )

        if detokenize_response.status_code in self.exceptions:
            raise self.exceptions[detokenize_response.status_code]

        return detokenize_response.json()
