from collections import defaultdict
from datetime import datetime, timedelta

import pytz
from sqlalchemy.inspection import inspect


def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            if "voicemail_boxes" in key:
                result[key].append(x.value[0].vmb_name)
            else:
                result[key].append(x.value)
    return result


def get_current_time():
    """converting utc to ET"""
    return datetime.utcnow() - timedelta(hours=5)


def get_eastern_timezoneval():
    current_eastern_time = datetime.now(pytz.timezone("US/Eastern"))
    return current_eastern_time
