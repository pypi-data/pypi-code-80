from .framework._application import _app as app
import threading
import string
import os

packaet_manager_name = 'tppm'

packaet_readme_assets = """testcanarybot assets
Copyright 2021 kensoi

Usage: with tools.assets(*args) as file: #like open(*args, **kwargs)
    #file usage"""
packaet_readme_library = """testcanarybot library
Copyright 2021 kensoi

Create module: python testcanarybot --project {packaet_project_directory} --cm {MODULENAME}"""

packaet_root_raw = """'''
testcanarybot project root
Copyright 2021 kensoi

This is raw created root file for testcanarybot project.
fill all important info and try to run with "$ python testcanarybot --run [LIST OF PROJECT DIRECTORIES]"

'''

import testcanarybot

community_name = 'Канарейка чан'
community_token = '{token}'
community_id = {group}

community_service = '{service_token}' # optional
apiVersion = '5.130'    # optional
countThread = 10        # optional

mentions = []
ALL_MESSAGES = False
ADD_MENTIONS = False
LISTITEM = '*'

LOGLEVEL = "INFO"       # CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET


if testcanarybot.root_init(__name__, __file__): # False -> it was launched through tppm
    bot = testcanarybot.app(
        accessToken = community_token,
        groupId = community_id,
        serviceToken = community_service, apiVersion = apiVersion, countThread = countThread, level = LOGLEVEL)

    bot.setMentions(mentions)

    bot.tools.values.set("ALL_MESSAGES", ALL_MESSAGES)
    bot.tools.values.set("ADD_MENTIONS", ADD_MENTIONS)
    bot.tools.values.set("LISTITEM", LISTITEM)

    bot.start_polling()
"""

libraryModuleRaw = """'''
library module raw script
Copyright 2021 kensoi
'''
from testcanarybot import objects


class Main(objects.libraryModule):
    async def start(self, tools: objects.tools):
        pass # create task at start
        @objects.ContextManager(commands = [\"check\"])


    async def ContextManagerHandler(self, tools: objects.tools, package: objects.package):
        await tools.api.message.send(
            random_id = tools.gen_random(), 
            peer_id = package.peer_id, 
            message = "Hello world!"
            )
"""


def system_message(*args):
    print(packaet_manager_name, '>>', *args)

def gen_str(test = None):
    result, num = "", random.randint(5, 25)

    if isinstance(test, int):
        num = test

    while num != 0:
        result += random.choice([
                *string.ascii_lowercase,
                *string.digits]
        )
        num -= 1
    return result

def parsename(name: str):
    name = name.lower()
    test, i = len(name), 0
    while i< test:
        if name[i] not in [
                *string.ascii_lowercase,
                *string.digits]:
            name = name[:i] + name[i+1:]
            test -= 1

        else:
            i+= 1

    if name == '': name = 'module_' + gen_str()
    
    return name

def getProjects(path: str):
    projects = []

    for directory in os.listdir(path):
        if os.path.isdir('\\'.join([path,directory])) and directory not in ['testcanarybot', 'docs', 'tools', 'all', 'info', 'assets', 'library']:
            if 'root.py' in os.listdir('\\'.join([path, directory])) and 'assets' in os.listdir('\\'.join([path, directory])) and 'library' in os.listdir('\\'.join([path, directory])):
                if not os.path.isdir('\\'.join([path, directory, 'root.py'])) and os.path.isdir('\\'.join([path, directory, 'assets'])) and os.path.isdir('\\'.join([path, directory, 'library'])):
                    projects.append(directory)

    return projects

class threadBot(threading.Thread):
    def __init__(self, data, botname, assets, library):
        threading.Thread.__init__(self)
        self.botname = botname
        self.accessToken = data.community_token + ""
        self.groupId = data.community_id + 0
        self.serviceToken = "" if not hasattr(data, 'community_service') else data.community_service + ""
        self.apiVersion = "5.126" if not hasattr(data, 'apiVersion') else data.apiVersion + ""
        self.countThread = 5 if not hasattr(data, 'countThread') else data.countThread + 0

        self.all_messages = data.ALL_MESSAGES if hasattr(data, 'ALL_MESSAGES') else None
        self.listitem = data.LISTITEM if hasattr(data, 'LISTITEM') else None


        if hasattr(data, 'mentions'):
            self.mentions = data.mentions[:]
        else:
            self.mentions = []

        if hasattr(data, 'assets'):
            self.assets = data.assets
        else:
            self.assets = assets

        if hasattr(data, 'library'):
            self.library = data.library
        else:
            self.library = library

        self.start()

    def exception_handler(self, loop, context):
        print(traceback.format_exc())
        quit()


    def run(self):
        self.bot = app(
            self.accessToken, 
            self.groupId, 
            self.serviceToken, 
            self.apiVersion, 
            self.countThread, 
            self.botname + '\\' + self.assets, 
            self.botname + '\\' + self.library
            )
        if len(self.mentions) != 0: self.bot.setMentions(self.mentions)
        if self.all_messages: self.bot.tools.values.set("ALL_MESSAGES", self.all_messages)
        if self.listitem: self.bot.tools.values.set("LISTITEM", self.listitem)
        
        system_message("@" + self.bot.tools.getBotLink(), "initialised, started")
        self.bot.start_polling()