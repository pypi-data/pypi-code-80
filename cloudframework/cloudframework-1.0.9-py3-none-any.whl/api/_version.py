from cloudframework.RESTFul import RESTFul
import os
class API(RESTFul):

    def main(self):

        self.core.logs.add({'a':4,'b':5})
        res = {
            "self.core.version": self.core.version,
            "self.core.isThis.development()": self.core.isThis.development(),
            "self.core.isThis.production()": self.core.isThis.production(),
        }
        self.addReturnData(res)
