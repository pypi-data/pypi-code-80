import socket
from ServerCL.Constant.Const import Constant
from ServerCL.Response.Packer import PACKER as Packer


class ServerClient:

    def __init__(self, server_ip: str, server_port: int, max_bit_size: int = 2048):

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_ip = server_ip
        self.__server_port = server_port
        self.__max_receive_size = max_bit_size
        self.__logged_messages = []

    def console_log(self, message, prefix='(Client)'):

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

    def get_client(self) -> socket.socket:

        return self.__client

    def get_address(self):

        return self.get_server_ip(), self.get_server_port()

    def connect(self):

        self.console_log('Attempting to connect to server')

        try:

            self.get_client().connect(self.get_address())

            self.console_log('Established connection to server')

            return self.get_client().recv(self.get_max_receive_size()).decode()

        except Exception:

            pass

    def send_data(self, data_type: Constant, data):

        self.console_log(f'Attempting to send data: {data}')

        try:

            self.get_client().send(str.encode(Packer.pack(data_type, data)))

            self.console_log(f'Successfully sent data: {data}')

            server_response = self.get_client().recv(self.get_max_receive_size()).decode()

            if server_response:

                unpacked_response = Packer.unpack(server_response)

                self.console_log(f'Succesfully collected and unpacked response: {unpacked_response}')

            return server_response if server_response else None

        except socket.error as e:

            self.console_log(f'Error whilst trying to send information {e}')