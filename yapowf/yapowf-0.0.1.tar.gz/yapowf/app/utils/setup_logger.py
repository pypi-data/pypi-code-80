import logging

class Logger:

    def __init__(self):

        format="%(process)d-%(levelname)s-%(message)s"
        self.logging.basicConfig(format=format)

    def info(self, txt):
        return self.logging.info(txt)

    def warn(self, txt):
        return self.logging.warning(txt)

    def error(self, txt):
        return self.logging.error(txt)
