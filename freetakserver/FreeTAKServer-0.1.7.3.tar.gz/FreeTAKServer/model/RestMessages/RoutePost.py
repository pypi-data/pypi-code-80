from FreeTAKServer.model.RestMessages.Route import Route, RestEnumerations

class RoutePost(Route):
    def __init__(self):
        pass

    def setlatitude(self, latitude):
        self.latitude = str(latitude)

    def getlatitude(self):
        return self.latitude

    def getlongitude(self):
        return self.longitude

    def setlongitude(self, longitude):
        self.longitude = str(longitude)

    def setlatitudeDest(self, latitudeDest: str):
        self.latitudeDest = str(latitudeDest)

    def getlatitudeDest(self):
        return self.latitudeDest

    def getlongitudeDest(self):
        return self.longitudeDest

    def setlongitudeDest(self, longitudeDest):
        self.longitudeDest = str(longitudeDest)

    def getname(self):
        return self.name

    def setname(self, name):
        self.name = name

    def gettimeout(self):
        return self.timeout

    def settimeout(self, timeout):
        self.timeout = timeout

    def getaddress(self):
        return self.address

    def setaddress(self, address):
        self.address = address

    def getmethod(self):
        return self.method

    def setmethod(self, method):
        self.method = method