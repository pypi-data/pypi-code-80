from abc import ABC, abstractmethod

from modfy.ProcessServer import ProcessServer


class OperationClass(ABC):

    serverOperationJson: {}

    def __init__(self, **kwargs):
        self.inputFiles = kwargs['inputFiles']
        if 'isAsync' in kwargs and 'webhookUrl' in kwargs:
            self.server = ProcessServer(self, kwargs['isAsync'], kwargs['webhookUrl'])
        else:
            self.server = ProcessServer(self)

    def defaultExtension(self):
        ext = self.inputFiles[0].name.split('.').pop()
        return ext

    def process(self, token):
        return self.server.process(token)

    @abstractmethod
    def setServerOperation(self):
        pass
