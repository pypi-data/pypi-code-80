from Namespace import Namespace
import json
import http.client
from rci.Exceptions import RciError

class Client:
  def __init__(self, address, tpm=100):
    try: self.conn = http.client.HTTPConnection(address)
    except: raise RciNetworkError() from None
    self.providers = []
    self.sessionID = None
    self.tpm = tpm

  def _post(self, path, **kwargs):
    self.conn.request('POST', path, **kwargs)
    resp = self.conn.getresponse()
    if resp.status != 200:
      raise RciNetworkError() from None
    return Namespace.json(resp.read())

  def addProvider(taskID, provider):
    try: self.providers[taskID] += [provider]
    except KeyError: self.providers[taskID] = [provider]

  def close(self):
    self.conn.close()

  def tick(self):
    start = datetime.now()
    tasks = self._post('/PollTasksImage').tasks
    for task in tasks:
      try: providers = self.providers[task.ID]
      except KeyError: continue
      for provider in providers:
        provider.run(task)
    now = datetime.now()
    duration = now - start
    delay = (6e4/self.tpm - duration)
    if delay > 0:
      sleep(delay / 1000)

  def run(self):
    try:
      while True:
        self.tick()
    except KeyboardInterrupt:
      print(' * EXIT *')
      break
    self.close()
