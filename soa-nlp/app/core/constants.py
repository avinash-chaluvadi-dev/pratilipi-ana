from app.core.config import settings

LOGIN_BAD_REQUEST = "Invalid username or password"
GENERIC_BAD_REQUEST = "Invalid request. Please check your request data!"
TOPIC_CLASSIFIER_LIST_STRING_EXCEPTION = (
    "Please check your request data and pass either list or string"
)
NER_LIST_STRING_EXCEPTION = (
    "Please check your request data and pass either list or string"
)
NORMALIZATION_LIST_STRING_EXCEPTION = (
    "Please check your request data and pass either list or string"
)
GENERIC_INTERNAL_ERROR = "Something went wrong please contact system admin!"
GENERIC_FORBIDDEN_ERROR = "You don`t have privilege to perform this action"
JWT_INVALID_SCHEME = "Invalid authentication scheme."
JWT_INVALID_CODE = "Invalid authorization code."

APP_META = {
    "title": settings.APP_TITLE,
    "description": settings.APP_DESCRIPTION,
    "version": settings.APP_VERSION,
    "contact": settings.APP_CONTACT,
    "swagger_ui_parameters": {"defaultModelsExpandDepth": -1},
    "debug": settings.DEBUG,
}
