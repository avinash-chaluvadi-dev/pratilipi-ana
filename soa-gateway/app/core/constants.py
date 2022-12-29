LOGIN_BAD_REQUEST = "Invalid username or password"
GENERIC_BAD_REQUEST = "Invalid request. Please check the request data!"
GENERIC_INTERNAL_ERROR = "Something went wrong please contact system admin!"
GENERIC_FORBIDDEN_ERROR = "You don`t have privilege to perform this action"
GENERIC_RECORD_NOT_FOUND = "Record not found"
GENERIC_RECORD_ALREADY_EXIST = "Record already exist"
JWT_INVALID_SCHEME = "Invalid authentication scheme."
JWT_INVALID_CODE = "Invalid authorization code."
SORTLIST = ["membername", "reasoncall", "callnumber", "receivedtime"]
STATUS_FILTER = ["Overdue", "Pending", "InProgress", "Completed"]
RECEIVED_TIME = "receivedtime"
DEFAULT_LIMIT_COUNT = 20
DEFAULT_OFFSET_COUNT = 0
DB_ERROR = "DB connection failed"
DATA_NOT_FOUND_MESSAGE = "{} {} not found"
DATA_CONFLICT_MESSAGE = "{} {} already exist"
DATA_ERROR_LISTALL = "Record(s) not found"
EXCEL_REPORT_ERROR = "Unable to generate Report"
HEALTH_CHECK_LDAP_FAILED = "LDAP server failed to connect"
HEALTH_CHECK_DB_FAILED = "DB failed to connect"
PROTEGRITY_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}
UNAUTHORISED_ERROR_MESSAGE = "Unauthorised access"
NOT_ACCEPTABLE_ERROR = "Service not acceptable"
REQUEST_TIMEOUT_ERROR = "Request timeout error"
VOICEMAIL_SET_ERROR = "Voicemail id/uuid is missing"
UNAVAILABLE_FOR_LEGAL_REASONS = "REPORT NOT GENERATED UNAVAILABLE FOR LEGAL REASONS"
STATE_FILTER = ["Pending", "InProgress", "Completed", "Overdue"]
INVALID_NER_ENTRY = "Entities are missing in NER value"
EXPORT_REPORT_COLUMNS = [
    "Voicemail box name",
    "Voicemail id",
    "Voicemail name",
    "Voicemail received date",
    "Voicemail received time",
    "Member Message",
    "Member name",
    "Extension ID",
    "Voicemail Current Status",
    "Call back number",
    "Reason for call",
    "Member called back",
    "Callback number reachable",
    "Voicemail Duration",
    "Voicemail reviewer Name",
    "Review comments",
    "Review Start date",
    "Review End date",
    "Is Overdue",
]
PROTEGRITY_SERVER_FAILED = "Protegrity server is not responding"
PROTEGRITY_SAMPLE_INPUT = [{"Name": "Legato"}]
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "pool_size": 5,
    "pool_timeout": 5,
    "isolation_level": "AUTOCOMMIT",
}
PROTEGRITY_MAPPING = {
    "vm_name": "Name",
    "vm_member_name": "firstName",
    "vm_callback_no": "SSN",
    "vm_extension_id": "OtherID",
    "vm_transcript_dtls": "B64_ENCRYPTION",
    "vm_normalized_dtls": "B64_ENCRYPTION",
}
SUCCESS_RESPONSE_CODE = [201, 204, 200]
REQUEST_ID_CTX_KEY = "request_id"
REVIEWER_COMMENTS_LIMIT = 1000
