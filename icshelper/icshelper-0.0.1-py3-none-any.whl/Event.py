from uuid import uuid1
import datetime


class Event:
    def __init__(self, paramenter: dict):
        self.event = dict()
        self.TIMEZONE = "Asia/Shanghai"
        self.event['DTSTART;TZID=' + self.TIMEZONE] = paramenter['DTSTART']
        self.event['DTEND;TZID=' + self.TIMEZONE] = paramenter['DTEND']
        self.event['DTSTAMP'] = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
        self.event['UID'] = str(uuid1())
        self.event['CREATED'] = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
        self.event['DESCRIPTION'] = paramenter['DESCRIPTION']
        self.event['LAST-MODIFIED'] = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
        self.event['STATUS'] = "CONFIRMED"
        self.event['SUMMARY'] = paramenter['SUMMARY']
        self.event['TRANSP'] = "OPAQUE"

    def __str__(self):
        return_string = str()

        return_string += "BEGIN:VEVENT\n"

        for key, value in self.event.items():
            return_string += key + ":" + value + "\n"

        return_string += "END:VEVENT\n"

        return return_string
