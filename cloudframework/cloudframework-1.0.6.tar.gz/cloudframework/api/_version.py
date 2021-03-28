from cloudframework.RESTFul import RESTFul

class API(RESTFul):

    def main(self):

        self.core.logs.add({'a':4,'b':5})
        res = {
            "Description": "Hello World",
            "Version": self.core.version,
            "request.form": self.formParams,
            "system.url": self.core.system.url,
            "core.errors": self.core.errors.data
        }
        self.addReturnData(res)
