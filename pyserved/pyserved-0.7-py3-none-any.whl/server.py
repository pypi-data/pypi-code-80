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
import threading
import os
import getpass
import random
import errno
# import netifaces as ni

username = getpass.getuser()


# try:
#     os.mkdir(f"Users/{username}/.pyserved/")
# except:
#     pass

import platform; osofmachine = platform.system().lower()

if osofmachine == "windows":
    SAVE_DIR = r"C:\Users\{username}\pyserved".format(username=username)
elif osofmachine=="darwin":
    SAVE_DIR = f"/Users/{username}/pyserved"
elif osofmachine=="linux":
    SAVE_DIR = f"/Users/{username}/pyserved"

# SAVE_DIR = f'/Users/{username}/pyserved'

try:
    os.mkdir(SAVE_DIR)
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise
    pass


random_num = random.randint(1000, 9999)
name = f"copiedfile{random_num}"

# ni.ifaddresses('eth0')
print("______________________________________________________")
print("")
if osofmachine == 'darwin' or osofmachine == 'linux':
    print("You can find out the ip address by typing\n \n $ ifconfig en1 \n\n or \n\n $ ifconfig en0\n\n or you can search google for it.\n\n")
elif osofmachine=="windows":
    print("You can find out the ip address by using \n \n $ ipconfig \n\n")

SERVER = input('Server HOST on which you want to run: ')

# SERVER = socket.gethostbyname(socket.getfqdn())

clients = []
HEADER = 64
PORT = int(input('PORT: '))
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!q"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr[0]}:{addr[1]} connected")

    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            # print(msg_length)
            msg_length = int(msg_length)
            msg = conn.recv(int(100000000)).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[{addr[0]}:{addr[1]}] has disconnected")
                # conn.send("You have been disconnected".encode(FORMAT))

            # print(f"[{addr[1]}] {msg}")

            filetype = msg.split("*-*/")[0].split(".")[1]
            content = msg.split("*-*/")[1]

            f = open(f'{SAVE_DIR}/{name}.{filetype}', 'w+')
            f.write(content)
            f.close()

            conn.send("200".encode(FORMAT))

    conn.close()


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        clients.append((conn, addr))
        # print(clients)
        # print(f"[NEW CONNECTION] Client with ip {addr[0]}:{addr[1]} has connected to your server.")

        if threading.activeCount() - 1 > 3:
            print("[ERROR] More than 2 clients are not allowed.")

        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def startserver():
    print(f"[STARTING] SERVER is starting on {str(SERVER)}:{str(PORT)}")
    print(f"[RUNNING] Server is succesfully running....")
    print(
        f"[RUNNING] The files which will be sent to you will be saved on {SAVE_DIR} directory.")
    start()

print("______________________________________________________")
startserver()
