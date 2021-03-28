import socket, sys

s = socket.socket()
for line in open(sys.argv[1]):
  if 'server: ' in line:
    host, port = line.split(': ')[1].split('->')
    s.bind((host, int(port)))
    s.listen(1)
  if 'send: ' in line:
    sendmsg = line.split(': ')[1]
    while 1:
      conn, addr = s.accept()
      conn.sendall(b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'+sendmsg.encode())
