import logging

logger = logging.getLogger(__name__)

class BaseConnector:
    '''Connector base class.'''
    def __init__(self, target='127.0.0.1' , port:int=22, username:str='', password:str='',  timeout:int=10):
        self.target = target
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout

    def __connect():
        pass

    def __close():
        pass

class SSHConnector(BaseConnector):
    '''SSH plugins base class. Implements:
    connect()
    close()
    send_commands()'''

    def __connect(self):
        logger.critical('Connecting to {} needs implementation PARAMIKO.'.format(self.target))
             
    def __close(self):
        logger.critical('Closing {} needs implementation.'.format(self.target))

    def send_commands(self, commands:list):
        self.__connect()
        for command in commands:
            logger.critical('Sending command "{}" needs implementation.'.format(command))
        self.__close()

class TunnelSSHConnector(SSHConnector):
    '''SSH plugins base class. Implements:
    connect()
    close()
    send_commands()'''
    def __init__(self, target='127.0.0.1' , port:int=22, username:str='', password:str='',  timeout:int=10,
                 use_jumphost = False, jumphost_ip='127.0.0.1' , jumphost_port:int=22, 
                 jumphost_username:str='', jumphost_password:str='',  jumphost_timeout:int=10):
        super().__init__(target, port, username, password, timeout)
        self.use_jumphost = use_jumphost
        self.jumphost = SSHConnector(jumphost_ip, jumphost_port, jumphost_username, jumphost_password,
                                      jumphost_timeout)

    def __connect(self):
        '''Private function connect to device'''
        logger.critical('Open SSH tunnel to {}  via {} needs implementation.'.format(self.target, self.jumphost.target))
        logger.critical('Connecting to {} needs implementation PARAMIKO.'.format(self.target))
        
    def __close(self):
        '''Private function close connection'''
        logger.critical('Closing {} needs implementation.'.format(self.target))
        logger.critical('Close Tunnel')

    def send_commands(self, commands:list):
        self.__connect()
        for command in commands:
            logger.critical('Sending command "{}" needs implementation.'.format(command))
        self.__close()
