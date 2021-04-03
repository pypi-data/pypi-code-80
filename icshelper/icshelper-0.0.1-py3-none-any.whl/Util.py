import datetime
from Event import Event


def genEventsByWeeks(paramenter: dict, start_time: datetime, end_time:datetime , weeks: list):
    ret = list()
    for i in weeks:
        event_para = paramenter
        event_para["DTSTART"] = (start_time + datetime.timedelta(weeks=(i - 1))).strftime("%Y%m%dT%H%M%S")
        event_para["DTEND"] = (end_time + datetime.timedelta(weeks=(i - 1))).strftime("%Y%m%dT%H%M%S")
        event = Event(event_para)
        ret.append(event)

    return ret
