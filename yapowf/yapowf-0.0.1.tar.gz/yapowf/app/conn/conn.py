import os
import sys
# from ..utils.setup_logger import logger

import logging

logging.basicConfig(level=logging.DEBUG, 
                    format="%(levelname)s - %(message)s")
logger = logging.getLogger()


class PowerFactoryConn:

    def __init__(self, 
                 path, 
                 username,
                 password,
                 logger=logger):

        self.path = path
        self.username = username
        self.password = password
        self.logger = logger
        
        self.check_path()
        self.check_credentials()

    def check_path(self):
        if not os.path.isdir(self.path):
            raise Exception("Invalid power factory python directory")

    def check_valid_conn(self, app):
        if app is None:
            raise Exception("Power Factory Connection failed.. please check your credentials")
        else:
            self.logger.info("Power Factory connected sucessfully")
    
    def check_credentials(self):
        if not self.username:
            raise Exception(":: Username must be provided")
        if self.password is None:
            self.logger.warning("Password not provided")

    def connect(self):

        try:
            sys.path.append(f"{self.path}")
            
            import powerfactory
            logger.info("Logging to Power Factory.. please wait")        
            app = powerfactory.GetApplication(self.username,
                                              self.password)
            self.check_valid_conn(app)
            self.logger.info("Connected with user -{}-".format(self.username))
         
        except Exception as e:
            print(e)
        
        return app