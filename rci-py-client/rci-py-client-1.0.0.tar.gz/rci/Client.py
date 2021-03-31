import http.client

class Client:
  def __init__(self):
    conn = http.client.HTTPConnection('127.0.0.1:700')
    conn.request('POST', '/PollTasksImage')
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    data = r1.read()
    print(data)
    conn.close()
