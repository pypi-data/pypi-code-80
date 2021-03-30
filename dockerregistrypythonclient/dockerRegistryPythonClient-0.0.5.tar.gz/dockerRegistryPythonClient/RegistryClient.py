import PythonAPIClientBase
from .RegistryLoginSession import RegistryLoginSessionBasedOnBasicAuth
from .RegisteryIterator import RegisteryIterator, genFnCollectSinglePageFunction
import json

class RegistryClient(PythonAPIClientBase.APIClientBase):

  def __init__(self, baseURL, mock=None):
    super().__init__(baseURL=baseURL, mock=mock, forceOneRequestAtATime=True)

  def getLoginSessionBasedOnBasicAuth(self, username, password):
    return RegistryLoginSessionBasedOnBasicAuth(APIClient=self, username=username, password=password)

  def getBase(self, loginSession):
    result = self.sendGetRequest(
      url="/v2/",
      loginSession=loginSession
    )
    if result.status_code != 200:
      self.raiseResponseException(result)

    return json.loads(result.content)

  def getCatalogIterator(self, loginSession):
    def retrieveListFromResponse(responseJSON):
      return responseJSON["repositories"]

    def itemGeneratorFunction(responseFromAPI):
      # Each item is just a string
      return responseFromAPI

    return RegisteryIterator(
      itemGeneratorFunction=itemGeneratorFunction,
      collectSinglePageFunction=genFnCollectSinglePageFunction(
        apiClient=self, loginSession=loginSession, pageSize=100, baseAPI="/v2/_catalog",
        retrieveListFromResponseFn=retrieveListFromResponse
      )
    )

  def getTagsForCatalogIterator(self, loginSession, catalogName):
    def retrieveListFromResponse(responseJSON):
      return responseJSON["tags"]

    def itemGeneratorFunction(responseFromAPI):
      # Each item is just a string
      return responseFromAPI

    return RegisteryIterator(
      itemGeneratorFunction=itemGeneratorFunction,
      collectSinglePageFunction=genFnCollectSinglePageFunction(
        apiClient=self, loginSession=loginSession, pageSize=100, baseAPI="/v2/" + catalogName + "/tags/list",
        retrieveListFromResponseFn=retrieveListFromResponse
      )
    )

# TODO Investigate https://forums.docker.com/t/get-image-digest-from-remote-registry-via-api/9480
