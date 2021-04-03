import json

# Class for any kind of iterator used with docker registry API

class RegisteryIterator:
  loginSession = None
  curList = None
  curIdx = None
  curOffset = None
  context = None

  # function given an api response value will return the object that the iterator returns
  itemGeneratorFunction = None

  # function that will get the next page of results from the api
  #  - input: curOffset = current offset of iterator
  #  - returns LIST of the items that are in the iterator
  collectSinglePageFunction = None

  def __init__(self, itemGeneratorFunction, collectSinglePageFunction):
    self.itemGeneratorFunction = itemGeneratorFunction
    self.collectSinglePageFunction = collectSinglePageFunction

    self.curList = []
    self.curIdx = 0
    self.curOffset = 0
    self.context = {}

  def __iter__(self):
    self.curList = []
    self.curIdx = 0
    self.curOffset = 0
    self.context = {}
    return self

  def __next__(self):
    if self.curIdx >= len(self.curList):
      self.collectNextPage()
      if self.curIdx >= len(self.curList):
        raise StopIteration
    cur = self.curIdx
    self.curIdx += 1
    return self.itemGeneratorFunction(responseFromAPI=self.curList[cur])

  def collectNextPage(self):
    self.curList = self.collectSinglePageFunction(self.curOffset, self.context)
    if self.curList is None:
      self.curList = []
    self.curIdx = 0
    self.curOffset += len(self.curList)



def genFnCollectSinglePageFunction(apiClient, loginSession, pageSize, baseAPI, retrieveListFromResponseFn):
  def collectSinglePageFunction(curOffset, context):
    urlToCall = ""
    if "stop" in context:
      return []

    if "link" in context:
      urlToCall = context["link"]
    else:
      # Must be first time function is called
      urlToCall = baseAPI + "?n=" + str(pageSize)

    result = apiClient.sendGetRequest(
      url=urlToCall,
      params=None,
      loginSession=loginSession
    )
    context["link"] = None
    if "Link" not in result.headers:
      context["stop"] = True
    else:
      if result.headers["Link"].startswith("<"):
        if result.headers["Link"].endswith(">; rel=\"next\""):
          context["link"] = result.headers["Link"].lstrip("<").rstrip(">; rel=\"next\"")
      if context["link"] is None:
        raise Exception("Bad link header")

    if result.status_code != 200:
      apiClient.raiseResponseException(result)

    resultJSON = json.loads(result.content)

    return retrieveListFromResponseFn(resultJSON)
  return collectSinglePageFunction