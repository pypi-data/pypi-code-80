import os
import sys
import logging
import pprint
from .python_connectors import TunnelSSHConnector

logger = logging.getLogger(__name__)

class BasePythonPlugin:
    '''Base class for Rundeck python plugin'''
    def __init__(self):
        self.condition = os.environ.get('RD_CONFIG_CONDITION', 'Always')
        self.a_var = os.environ.get('RD_CONFIG_A_VAR')
        self.b_var  = os.environ.get('RD_CONFIG_B_VAR')
        self.check_conditionals()
        self.output = {}
        debug_level = os.environ.get('RD_CONFIG_DEBUG_LEVEL', 'ERROR')
        level = logging.getLevelName(debug_level)
        if os.environ.get('RD_JOB_LOGLEVEL') == 'DEBUG':
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=level)
        logger.debug('Condition set :'.format(self.condition))
        
    def check_conditionals(self):
        '''Check conditionals require execution. Exit if not.'''
        if self.condition == 'Always':
            pass
        elif self.condition == 'Never':
            self.output['warning'].append('Condition set to never. Step not executed.')
            sys.exit(0)

    def print_output(self, out_format:str='dict'):
        if isinstance(self.output, dict) and out_format == 'text':
            for k, v in self.output:
                print(k)
                print('  ', v)
        elif isinstance(self.output, dict) and out_format == 'dict':
            pprint.pprint(self.output, indent=4)
        elif isinstance(self.output, dict) and out_format == 'dict':
            print (self.output)
        else:
            print (self.output)


class SSHPythonPlugin(BasePythonPlugin):
    '''SSH connection to target.'''
    def __init__(self, target:str='', ssh_port:int=22, username:str='', password:str='',  timeout:int=10,
                 delay_start:float=0.5, command_interval:float=0.5,
                 jumphost_hostname:str='', jumphost_port:int='22', 
                 jumphost_username:str='', jumphost_password:str=''):
        self.ssh = TunnelSSHConnector(target, ssh_port, username, password, timeout, True,
                                      jumphost_ip=jumphost_hostname, jumphost_port=jumphost_port,
                                      jumphost_username=jumphost_username, jumphost_password=jumphost_password )
        self.timeout = timeout
        super().__init__()

        
    def set_credentials(self, username:str, password:str):
        self.username = username
        self.password = password

    def set_target(self, target:str, ssh_port:int=22):
        self.target = target
        self.ssh_port = ssh_port

