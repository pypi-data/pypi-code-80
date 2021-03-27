
class BaseIFlowlyException(Exception): pass

class APIKeyMissing(BaseIFlowlyException): pass

class TriggerError(BaseIFlowlyException): pass


class InitialStateNotFound(BaseIFlowlyException): pass