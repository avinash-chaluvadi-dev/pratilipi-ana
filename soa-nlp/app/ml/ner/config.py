import re

regex_expression = {
    "MEMBER_ID": re.compile(r"[0-9]{3}[a-z|A-Z]{1}[0-9]{5}"),
    "CALLBACK_ID": re.compile(r"[\(]*[0-9]{3}[\)]*[-|\s|.]*[0-9]{3}[-|\s|.]*[0-9]{4}"),
    "DATE": re.compile(r"[0-9]{1,2}[-|/][0-9]{1,2}[-|/][0-9]{2,4}"),
}
spacy_model = "en_core_web_md"
