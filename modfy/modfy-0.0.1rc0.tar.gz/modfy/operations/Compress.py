from modfy.operations.OperationClass import OperationClass


class Compress(OperationClass):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputFiles = kwargs['inputFiles']
        self.compressValue = kwargs['compressValue']
        self.setServerOperation()

    def setServerOperation(self):
        self.serverOperationJson = {
            'type': 'compress',
            'from': self.defaultExtension(),
            'options': {
                'crf': self.compressValue
            }
        }
