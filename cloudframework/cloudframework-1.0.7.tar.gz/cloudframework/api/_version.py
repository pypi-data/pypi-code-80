from cloudframework.RESTFul import RESTFul
import os
class API(RESTFul):

    def main(self):

        self.core.logs.add({'a':4,'b':5})
        res = {
            "version": self.core.version,
            "is_development": self.core.isThis.development(),
            "is_production": self.core.isThis.production(),
        }
        print(os.environ)
        self.addReturnData(res)
