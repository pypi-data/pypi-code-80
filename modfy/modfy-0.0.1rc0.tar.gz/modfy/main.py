from modfy.auth import Auth
from modfy.operations import Compress


class Modfy:
    def __init__(self, token, secretToken):
        self.auth = Auth(token, secretToken)

    def __operation(self, Type, **kwargs):
        operator = Type(**kwargs)

        token = self.auth.getOneTimeToken()

        return operator.process(token)

    def compress(self, **kwargs):
        # TODO A way to transfer the argument types
        return self.__operation(Compress.Compress, **kwargs)
