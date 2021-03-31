import http.client
from rci.Exceptions import RciError

class Client:
  def __init__(self, address):
    self.conn = http.client.HTTPConnection(address)

  def getTasks(self):
    self.conn.request('POST', '/PollTasksImage')
    resp = self.conn.getresponse()
    if resp.status != 200:
      raise RciNetworkError()
    return resp.read()

  def close(self):
    self.conn.close()
