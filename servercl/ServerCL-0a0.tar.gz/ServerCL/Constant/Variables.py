from ServerCL.Constant.Const import Constant
import socket

""" Primal Constants """

CONSTANT_DATA_TYPE = Constant(10000)  # Interpreting constant data
SERVER_STARTED = Constant(100001)  # Server-side server started
SERVER_STOPPED = Constant(100002)  # Server-side server stopped

MACHINE_INTERNET_PROTOCOL = socket.gethostbyname(socket.gethostname())
MACHINE_IP = MACHINE_INTERNET_PROTOCOL


# Get an open port

def GET_OPEN_PORT(machine_ip: str = MACHINE_IP):
    sock = socket.socket()
    sock.bind((machine_ip, 0))

    open_port = sock.getsockname()[1]
    sock.close()

    return open_port


""" Data Types 10000-4 """

STRING = Constant(100010)  # Interpreting string data
INTEGER = Constant(100020)  # Interpreting integer data
FLOAT = Constant(100021)  # Interpreting float data
COMPLEX = Constant(100022)
LIST = Constant(100030)
TUPLE = Constant(100031)
RANGE = Constant(100032)
DICT = Constant(100040)
SET = Constant(100050)
FROZENSET = Constant(100051)
BOOLEAN = Constant(100060)  # Interpreting boolean Data
BYTES = Constant(100070)
BYTEARRAY = Constant(100071)
MEMORYVIEW = Constant(100072)

""" Server-side triggers 10005* """

CLIENT_CONNECTED = Constant(100080)  # Server-side connected to client
CLIENT_DISCONNECTED = Constant(100081)  # Server-side disconnected from client
CLIENT_LOST_CONNECTION = Constant(100082)  # Server-side lost connection to client
CLIENT_SHUTDOWN = Constant(100083)  # Server-side client shutdown
CLIENT_INFORMATION_RECEIVED = Constant(100084)  # Server-side received information from client

""" Client-side triggers 10006* """

SERVER_CONNECTED = Constant(100090)  # Client-side connected to server
SERVER_DISCONNECTED = Constant(100091)  # Client-side disconnected from server
SERVER_LOST_CONNECTION = Constant(100092)  # Client-side lost connection to server
SERVER_SHUTDOWN = Constant(100093)  # Client-side server shutdown
SERVER_INFORMATION_RECEIVED = Constant(100094)  # Client-side received information from server
