from PythonAPIClientBase import LoginSession, APIClientException
from base64 import b64encode

class RegistryLoginSessionBasedOnBasicAuth(LoginSession):
  username = None
  password = None
  apiClient = None

  def __init__(self, APIClient, username, password):
    self.apiClient = APIClient
    self.username = username
    self.password = password

  def testValid(self):

    try:
      response = self.apiClient.getBase(loginSession = self)
    except APIClientException as err:
      if err.result.status_code != 401:
        raise err
      # 401 returned auth must not be valid
      return False


    return True

  def injectHeaders(self, headers):
    userAndPass = b64encode((self.username + ":" + self.password).encode()).decode("ascii")
    headers["Authorization"] = "Basic " + userAndPass

  def refresh(self):
    pass
