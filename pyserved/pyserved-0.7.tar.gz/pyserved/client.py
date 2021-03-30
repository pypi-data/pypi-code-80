"""
________________________________
|                              |
| pyserved                     |
|                              |
| Only works with utf-8        | 
| files. (for now.)            |
|                              | 
| By:                          |
| Shaurya Pratap Singh         |
| 2021 ©                       |
|______________________________|
"""

import socket
import pickle
# import netifaces as ni

# def client():
HEADER = 64

print("______________________________________________________")
print("                                                ")
print("Pyserved CLI Client")
print("")
print("Enter the host and port in the fields below.")

# PORT = 5050

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!q"
# SERVER = "192.168.1.20"
# SERVER = socket.gethostbyname(socket.gethostname())
# host_name = socket.gethostname()
# SERVER = socket.gethostbyname(host_name + ".local")

SERVER = input('Server HOST: ')
PORT = int(input('PORT: '))
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)

    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    recv_msg = client.recv(100000000).decode(FORMAT)

    if recv_msg == "200":
        success = True
    else:
        success = False

    return success


"""

Socket DONE
main coding START

"""


def read(file):
    f = open(file, 'r')
    text = f.read()
    f.close()
    return file+"*-*/"+text

# file_path = input("File path: ")


def clientd(file_path):
    text = read(file_path)
    send(text)

print("Now enter the path of file which you want to send")
path = input("File path:")
clientd(path)

print("")
print("______________________________________________________")