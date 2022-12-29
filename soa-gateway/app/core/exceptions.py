from . import constants


class BaseException(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super(BaseException, self).__init__(message)


class BadRequestException(BaseException):
    def __init__(self, message=constants.GENERIC_BAD_REQUEST) -> None:
        super(BadRequestException, self).__init__(message)


class InternalServerError(BaseException):
    def __init__(self, message=constants.GENERIC_INTERNAL_ERROR) -> None:
        super(InternalServerError, self).__init__(message)


class ForbiddenException(BaseException):
    def __init__(self, message=constants.GENERIC_FORBIDDEN_ERROR) -> None:
        super(ForbiddenException, self).__init__(message)


class RecordNotFound(BaseException):
    def __init__(self, message=constants.GENERIC_RECORD_NOT_FOUND) -> None:
        super(RecordNotFound, self).__init__(message)


class RecordAlreadyExists(BaseException):
    def __init__(self, message=constants.GENERIC_RECORD_ALREADY_EXIST) -> None:
        super(RecordAlreadyExists, self).__init__(message)


class UnauthorisedError(BaseException):
    def __init__(self, message=constants.UNAUTHORISED_ERROR_MESSAGE) -> None:
        super(UnauthorisedError, self).__init__(message)


class NotAcceptableError(BaseException):
    def __init__(self, message=constants.UNAUTHORISED_ERROR_MESSAGE) -> None:
        super(NotAcceptableError, self).__init__(message)


class RequestTimeoutError(BaseException):
    def __init__(self, message=constants.UNAUTHORISED_ERROR_MESSAGE) -> None:
        super(RequestTimeoutError, self).__init__(message)


class GenerateReportException(BaseException):
    def __init__(self, message=constants.UNAVAILABLE_FOR_LEGAL_REASONS) -> None:
        super(GenerateReportException, self).__init__(message)
