import datetime


class fsak:
    def __init__(self):
        self.dt = datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=6)))

    def help(self):
        return f"{str(self.dt)}"


def execute():
    print(fsak().help())