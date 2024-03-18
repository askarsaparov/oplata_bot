from datetime import datetime, timedelta

import pytz

from db import select_need_payments


def timestamp_to_datetime(timestamp):
    timestamp = timestamp / 1000
    return datetime.fromtimestamp(timestamp, tz=pytz.timezone('Asia/Tashkent'))


