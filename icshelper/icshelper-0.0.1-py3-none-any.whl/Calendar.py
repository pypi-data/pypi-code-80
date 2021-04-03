class Calendar:
    cal = dict()
    events = list()

    def __init__(self):
        self.cal['PROID'] = "icshelper"
        self.cal['VERSION'] = "2.0"
        self.cal['CALSCALE'] = "GREGORIAN"
        self.cal['METHOD'] = "PUBLISH"
        self.cal['CLASS'] = "PUBLIC"

    def __str__(self):
        return_string = str()

        return_string += "BEGIN:VCALENDAR\n"

        for key, value in self.cal.items():
            return_string += key + ":" + value + "\n"

        for event in self.events:
            return_string += str(event)

        return_string += "END:VCALENDAR\n"

        return return_string

    def addEvents(self, events: list):
        self.events.extend(events)
