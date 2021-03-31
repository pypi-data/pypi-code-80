from logging import getLogger, basicConfig, INFO  # Ignore PyCharm errors
from logging.handlers import RotatingFileHandler


class Borg(object):
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state


class LogBorg(Borg):
    basicConfig(level=INFO)

    _logger = None

    def __init__(self):
        Borg.__init__(self)
        if self._logger is None:
            self._logger = getLogger('connexion.app')

            try:
                # Somehow necessary to avoid import errors
                from mosaik_schedule_flocker.schedule_flocker.util.paths \
                    import LOG_FILE_PATH

                handler = RotatingFileHandler(
                    filename=LOG_FILE_PATH,
                    maxBytes=10000,
                    backupCount=1,
                )
            except FileNotFoundError:
                # We are running in /test or /flocker
                log_file_path = '../logs/app.log'
                handler = RotatingFileHandler(
                    filename=log_file_path,
                    maxBytes=10000,
                    backupCount=1,
                )
            handler.setLevel(INFO)

            self._logger.addHandler(handler)

    @property
    def logger(self):
        return self._logger
