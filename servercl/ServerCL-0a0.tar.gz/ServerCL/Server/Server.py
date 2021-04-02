import socket
import _thread
from ServerCL.Constant.Const import Constant
from ServerCL.Constant.Variables import *
from ServerCL.Response.Packer import PACKER as Packer

class Server:

    def __init__(self, server_ip: str, port: int, max_bit_size: int = 2048):

        self.__server_ip = server_ip
        self.__server_port = port
        self.__max_receive_size = max_bit_size

        self.__events = {}

        self.__logged_messages = []

    def console_log(self, message, prefix='(Server)'):

        console_message = f'<{prefix}> Console.) {message}'
        self.__logged_messages.append(console_message)

        print(console_message)

    def get_server_ip(self):

        return self.__server_ip

    def get_server_port(self):

        return self.__server_port

    def set_max_receive_size(self, new_max_receive_size):

        self.__max_receive_size = new_max_receive_size

    def get_max_receive_size(self):

        return self.__max_receive_size

    """ Events """

    def get_events(self):

        return self.__events

    def get_event(self, event):

        return self.__events[event]

    def register_event_trigger(self, event_listener, event_trigger):

        if event_listener not in self.get_events():

            self.get_events()[event_listener] = []

        # Make sure to make it an empty list of functions

        self.get_events()[event_listener].append(event_trigger)

    def __trigger_event(self, event_triggered, *extra_data):

        if event_triggered in self.get_events():

            [event_trigger(self, *extra_data) for event_trigger in self.get_event(event_triggered)]

    """ Connection tool """

    def send_packed(self, connection, packing_type: Constant, information):

        connection.sendall(str.encode(Packer.pack(packing_type, information)))

    def __threaded_client(self, connection, address):

        while True:

            try:

                information = connection.recv(self.get_max_receive_size())  # Maximum received information in bits
                information = information.decode('utf-8')  # Information needs to be decoded into a string

                if not information:

                    self.console_log('Client disconnected', address)

                    self.__trigger_event(CLIENT_DISCONNECTED)

                    break

                else:

                    self.console_log(f'Received information: {Packer.unpack(information)}', address)

                    self.__trigger_event(CLIENT_INFORMATION_RECEIVED, connection, information) # Trigger that we received information from the client

            except IndexError:

                print('Connection closing since client from connection didn\'t send a support data type causing an index error, see documentation')

        self.console_log(f'Lost connection', address)
        connection.close()

    def start_server(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create new socket

        try:

            sock.bind((self.get_server_ip(), self.get_server_port()))  # Bind server to the port to reserve port

        except socket.error as e:

            self.console_log(f'Socket error occured: {e}')  # Socket binding error ( likely occupied )

        sock.listen(2)  # Open the socket to listen with arg as max connections
        self.console_log(f'Server started on IP: {self.get_server_ip()} & port: {self.get_server_port()}, awaiting connection')

        self.__trigger_event(SERVER_STARTED)  # Trigger that the server started up

        while True:

            connection, address = sock.accept()  # Establish a client connection if there is one
            self.console_log(f'Established connection', address)

            self.__trigger_event(CLIENT_CONNECTED, connection)  # Trigger that a client has connected with the connection

            _thread.start_new_thread(self.__threaded_client, (
                connection,
                address))  # Start a new thread so that ~simultaneous processes can happen for multiple connections
