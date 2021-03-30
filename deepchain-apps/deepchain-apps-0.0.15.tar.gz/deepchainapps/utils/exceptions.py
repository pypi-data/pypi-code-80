"""Module for custom exceptions"""


class DeepChainAppException(Exception):
    pass


class AppNotFoundError(DeepChainAppException):
    def __init__(self, app):
        super(AppNotFoundError, self).__init__(
            f"App {app} not found, you must create it "
            f"before deployement or specify correct name."
        )


class ConfigNotFoundError(DeepChainAppException):
    def __init__(self):
        super(ConfigNotFoundError, self).__init__(
            "Config File not found. You must login and register you PAT with :"
            / " >> deepchain login"
        )
