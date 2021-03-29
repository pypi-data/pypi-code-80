from typing import Dict, List, Tuple
import pendulum
from datetime import datetime


def to_local_time(date_utc: datetime, timezone: str = "Asia/Bangkok") -> datetime:
    tz = pendulum.timezone(timezone)
    date_utc = pendulum.instance(date_utc)
    target_date = tz.convert(date_utc)
    return target_date

def extract_date(execution_date_utc: datetime) -> Tuple[datetime, str, str, str]:
    execution_date = to_local_time(execution_date_utc)
    year = execution_date.format('YYYY')
    month = execution_date.format('MM')
    day = execution_date.format('DD')
    return execution_date, year, month, day