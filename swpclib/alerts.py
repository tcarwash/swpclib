import time
from datetime import datetime
import re


def format_message(alert):
    """Return a formatted alert message"""

    output = {}
    output["id"] = alert["product_id"]
    output["issue_datetime"] = datetime.strptime(
        alert["issue_datetime"], "%Y-%m-%d %H:%M:%S.%f"
    )
    output["message"] = alert["message"]
    #    _re_start_time = re.compile('^')

    #    output['start_time'] = _re_start_time.match(alert['message'])

    return output
