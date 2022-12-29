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
