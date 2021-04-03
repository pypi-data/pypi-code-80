

class ImageMetadata():
  _jsonDict = None
  _catalogName = None
  _tagName = None
  _dockerContentDigest = None

  def __init__(self, catalogName, tagName, jsonDict, dockerContentDigest):
    self._jsonDict = jsonDict
    self._catalogName = catalogName
    self._tagName = tagName
    self._dockerContentDigest = dockerContentDigest

  def getJson(self):
    return self._jsonDict

  def getQualifiedName(self):
    return self._catalogName + ":" + self._tagName

  def getDigest(self):
    return self._dockerContentDigest
    ### return self._jsonDict["config"]["digest"]

  def delete(self, registryClient, loginSession):

    # Delete calls must use digest not tag
    result = registryClient.sendDeleteRequest(
      url="/v2/" + self._catalogName + "/manifests/" + self.getDigest(),
      loginSession=loginSession,
      injectHeadersFn=None
    )
    if result.status_code != 202:
      registryClient.raiseResponseException(result)
