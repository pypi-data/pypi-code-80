from .. import exceptions
from .. import objects
from ..enums import values
from ..enums import events

from ._api import api
from ._threading import thread
from ._library import library as _library
from ._values import _ohr
from ._values import global_expressions

from datetime import datetime

import logging

import asyncio
import aiohttp
import atexit
import os
import threading
import time
import typing
import random

logger_levels = {
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10,
    'NOTSET': 0
}

class _assets:
    def __init__(self, assets = os.getcwd() + '\\assets'):
        self.__path = assets + '\\'


    def __call__(self, *args, **kwargs):
        args = list(args)
        if len(args) > 0:
            args[0] = self.__path + args[0]
        
        elif 'file' in kwargs:
            kwargs['file'] = self.__path + kwargs['file']
        
        return open(*args, **kwargs)


    def __exit__(self, exc_type, exc_value, traceback):
        pass


class async_sessions():
    """
    wrapper over about aiohttp.request() to avoid errors about loops in threads
    headers: dict()
    """

    def __init__(self, *args, **kwargs):
        self.__args = args
        self.__kwargs = kwargs
        self.__sessions = []


    def create_session(self, thread: threading.Thread) -> None:
        if not hasattr(thread, 'session'): 
            thread.session = aiohttp.ClientSession(*self.__args, **self.__kwargs)
            self.__sessions.append(thread.session)


    def __del__(self):
        for session in self.__sessions:
            asyncio.get_event_loop().run_until_complete(session.close())
        

    def __getattr__(self, name):
        if name in dir(aiohttp.ClientSession):
            thread = threading.current_thread()
            self.create_session(thread)
            return getattr(thread.session, name)


def _codenameToINT(int1: int, int2: int, int3: int) -> int:
    return int1 * 10000 + int2 * 1000 + int3


def _correctCodeName(int1: int, int2: int, int3: int) -> str:
    return f"{'%02d' % int1}.{'%02d' % int2}.{'%03d' % int3}"


class _app:  
    _headers = {
        'User-agent': """Mozilla/5.0 (Windows NT 6.1; rv:52.0) 
            Gecko/20100101 Firefox/52.0"""
    }


    __longpoll_url = ""
    __longpoll_ts = 0
    __longpoll_key = None

    __booted_once = False


    def __init__(self, 
        accessToken: str, groupId: int, serviceToken: str = "", 
        apiVersion: str = "5.126",  countThread: int = 1, 
        assets = 'assets', library = 'library', level: str = 'info', print_log:bool = False, logg = logging.Logger(name = "testcanarybot")):
        """
        testcanarybot project object

        # VK Bots API:

        accessToken [str] - token for community access [login/password for userbot is not supported]
        groupId [int] - group identificator
        serviceToken [str] - token for service access *Optional
        apiVersion [str] - set API version for your bot.

        # TESTCANARYBOT ADDITIONAL SETTINGS:

        countThread [int: 1] - set threads count for handlers.
        assets [str: "assets"] - current assets directory name (only name without path)
        library [str: "library"] - current library directory name (only name without path)
        logg [logging.Logger] - your logger
        level [str] - logging level [CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET]
        """
        self.logger = logg
        self.logger.setLevel(logger_levels[level.upper()])
        handler = logging.FileHandler("log.txt")
        self.logger.addHandler(handler)

        if threading.current_thread() == threading.main_thread():
            self.__loop = asyncio.get_event_loop()
            
        else:
            self.__loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.__loop)
        self.__loop

        self.__thread = []
        self.__access = accessToken
        self.__service = serviceToken
        self.__group_id = groupId
        self.__countThread = countThread
        self.__lastthread = 0
        self.__av = apiVersion
        self.__longpoll_delay = 1 / 20
        self.__longpoll_last = 0.0  

        self.__http = async_sessions(headers = self._headers)
        self.__api = api(self.__http, self.method)

        self.__tools = tools(self.__group_id, self.__api, self.__http, assets, self.logger, level, print_log)
        self.__tools.system_message(
            module = "session", 
            level = "info",
            write = self.tools.values.SESSION_START)
            
        self.__library = _library(self.tools, library)
        atexit.register(self.__close)


    @property
    def countThread(self):
        return self.__countThread

    @property
    def http(self):
        return self.__http

    @property
    def log(self):
        return self.logger.handlers[0].baseFilename

    @property
    def tools(self):
        return self.__tools

    @property
    def api(self):
        return self.__api

    @property
    def api_url(self):
        return "https://api.vk.com/method/"


    def __close(self):
        self.__tools.system_message(
            module = "session", 
            level = "info",
            write = self.__tools.values.SESSION_CLOSE)
        

    async def method(self, method: str, data: dict = {}):
        """ 
        raw API call

        method [str] - method name
        data [dict: {}] - parameters.
        """

        delay = self.__longpoll_delay - (time.time() - self.__longpoll_last)

        if 'group_id' in data: data['group_id'] = self.__group_id
        data['v'] = self.__av

        if 'type' in data:
            if data['type'] == 'service':
                data['access_token'] = self.__service
            
            else:
                data['access_token'] = self.__access
            
            del data['type']
        
        else:
            data['access_token'] = self.__access


        if delay > 0: await asyncio.sleep(delay)

        response = await self.http.post(self.api_url + method, data = data)
        response = await response.json()

        self.last_request = time.time()
        if 'error' in response: 
            raise exceptions.MethodError(f"[{response['error']['error_code']}] {response['error']['error_msg']}")

        return response['response']     


    def setMentions(self, mentions: list):
        """
        Setup custom mentions instead "@{groupadress}"
        """
        self.tools._tools__mentions = [self.tools._tools__group_mention, *[str(i).lower() for i in mentions]]


    def setup(self):  
        """
        [Optional] Install components to work with longpoll and your handlers.
        """  
          
        if len(self.__library.modules) == 0:
            self.__library.upload(self.__loop)

        time.sleep(0.01)
        self.logger.info(self.tools.values.LOGGER_START)

        if self.__countThread > len(self.__thread):
            for i in range(self.countThread):
                thread_started = thread(self.__library, i, threading.currentThread().getName())
                thread_started.start()
                
                self.__thread.append(thread_started)

        time.sleep(0.01)

        if not self.__booted_once:
            self.__booted_once = True

            for i in self.__library.modules.values():
                if hasattr(i, "start"): self.__getThread().create_task(i.start)

        self.__loop.run_until_complete(self.__update_longpoll_server())                


    def start_polling(self) -> None:
        """
        Start polling VK longpoll server for any events
        """

        self.setup()
        self.__library.tools.system_message(
            module = "longpoll",
            level = "debug",
            write = self.tools.values.LONGPOLL_START)
        self.__loop.run_until_complete(
            self.__pollingCycle())


    def check(self, times: int = 1) -> None:
        """
        Check VK longpoll server for any events for number of times.

        times [int : 1] - how many times you need to check.
        """

        self.setup()
        self.tools.system_message(
            module = 'longpoll',
            level = "debug",
            write = self.tools.values.LONGPOLL_START)
        
        while times != 0:
            times -= 1
            self.__loop.run_until_complete(self.__polling())
        
        self.tools.system_message(
            module = 'longpoll',
            level = "debug",
            write = self.tools.values.LONGPOLL_CLOSE)


    async def __update_longpoll_server(self, update_ts: bool = True) -> None:
        response = await self.method('groups.getLongPollServer', {'group_id': self.__group_id})

        if update_ts: self.__ts = response['ts']
        self.__longpoll_key, self.__longpoll_url = response['key'], response['server']

        if self.tools.values.DEBUG_MESSAGES:
            self.tools.system_message( 
                module = "longpoll",
                level = "debug",
                write = self.tools.values.LONGPOLL_UPDATE)


    async def __check(self):
        values = {
            'act': 'a_check',
            'key': self.__longpoll_key,
            'ts': self.__longpoll_ts,
            'wait': 25,
        }
        
        response = await self.http.get(
            self.__longpoll_url,
            params = values
        )
        response = await response.json(content_type = None)

        if 'failed' not in response:
            self.__longpoll_ts = response['ts']
            return response['updates']

        elif response['failed'] == 1:
            self.__longpoll_ts = response['ts']

        elif response['failed'] == 2:
            await self.__update_longpoll_server(False)

        elif response['failed'] == 3:
            await self.__update_longpoll_server()

        return []


    async def __pollingCycle(self):
        while True: await self.__polling()


    async def __polling(self):
        for event in await self.__check():
            if event['type'] == 'message_new':
                package = objects.package(event['object']['message'])
                package.params.client_info = objects.data(event['object']['client_info'])
                package.params.from_chat = package.peer_id > 2000000000

            else:
                package = objects.package(event['object'])

            package.type = getattr(events, event['type'])
            package.event_id = event['event_id']
            package.items = []
            self.__getThread().create_task(package)

        
    def __getThread(self):
        self.__lastthread = 0 if self.__lastthread + 1 == len(self.__thread) else self.__lastthread + 1
        return self.__thread[self.__lastthread]


    def test_parse(self, event: objects.package):
        """
        Init test parsing with received event 
        """
        self.setup()
        self.__getThread().create_task(event)




class tools:
    def __init__(self, group_id, api, http, assets, logger, level, print_log):
        self.__assets = _assets(os.getcwd() + '\\' + assets)
        
        self.__logger = logger
        self.__log_level = level
        self.__print_log = print_log

        self.__http = http
        self.__api = api
        self.__group_id = group_id
        self.__group_mention = ""

        self.__waiting_replies = {}
        self.__group_address = asyncio.get_event_loop().run_until_complete(self.api.groups.getById(group_id=self.__group_id))[0].screen_name

        self.__group_mention = f'[club{self.__group_id}|@{self.__group_address}]'
        self.__mentions = [self.__group_mention]
        
        self.__values = global_expressions()

    @property
    def assets(self):
        return self.__assets

    @property
    def values(self):
        return self.__values

    @property
    def api(self):
        return self.__api

    @property
    def http(self):
        return self.__http

    def gen_random(self):
        return int(random.random() * 999999)

    def system_message(self, *args, write: typing.Optional[str] = None, module: str = "system", level:str = 'info'):
        if not write: 
            write = " ".join([str(i) for i in list(args)])

        self.__logger.log(logger_levels[level.upper()], f'[{level.upper()}]\t@{self.__group_address}.{module}: {write}')

        if self.__print_log and level.upper() == self.__log_level:
            print(f'[{level.upper()}]\t@{self.__group_address}.{module}: {write}')
            
    def getBotId(self):
        return self.__group_id + 0

    def getBotLink(self):
        return self.__group_address

    def getBotDogMention(self):
        """
        Get Mention as testcanarybot.objects.mention
        To get mention at format [id|string] use repr(tools.getBotDogMention())
        """
        return objects.mention(self.__group_id, "@" + self.__group_address)

    def getBotMentions(self):
        """
        get all mentions that you set as bot mentions at commands
        """
        return self.__mentions[:]
    

    def wait_check(self, package):
        if package.type == events.message_new:
            return f"${package.peer_id}_{package.from_id}" in self.__waiting_replies.keys()
        else:
            raise TypeError("Only message_new")


    async def wait_reply(self, package):
        if package.type == events.message_new:
            wait = f"${package.peer_id}_{package.from_id}"
            self.__waiting_replies[wait] = False

            while True:
                if self.__waiting_replies[wait]: 
                    return self.__waiting_replies.pop(wait)
                
                await asyncio.sleep(0)
        else:
            raise TypeError("Only message_new")


    async def getMention(self, page_id: int, name_case = "nom"):
        if name_case == 'link':
            if page_id > 0:
                return f'[id{page_id}|@id{page_id}]'

            elif page_id == self.__group_id:
                return self.__group_mention

            else:
                test = await self.__api.groups.getById(group_id = -page_id)
                return f'[club{-page_id}|@{test[0].screen_name}]'
        
        else:
            if page_id > 0:
                request = await self.__api.users.get(
                    user_ids = page_id, 
                    name_case = name_case
                    )
                first_name = request[0].first_name
                
                return f'[id{page_id}|{first_name}]'
            
            elif page_id == self.__group_id:
                return self.mentions_self[name_case]
            
            else:
                request = await self.__api.groups.getById(
                    group_id = -page_id
                    )
                name = request[0].name
                
                return f'[club{-page_id}|{name}]' 


    async def getManagers(self, group_id = None):
        if not group_id:
            group_id = self.__group_id

        elif not isinstance(group_id, int):
            raise TypeError('Group ID should be integer')

        lis = await self.__api.groups.getMembers(group_id = group_id, sort = 'id_asc', filter='managers')
        return [i.id for i in lis.items if i.role in ['administrator', 'creator', 'moderator']]


    async def isManager(self, from_id: int, group_id = None):
        if not group_id:
            group_id = self.__group_id
            
        elif not isinstance(group_id, int):
            raise TypeError('Group ID should be integer')

        return from_id in await self.getManagers(group_id)


    async def getChatManagers(self, peer_id: int):
        res = await self.__api.messages.getConversationsById(peer_ids = peer_id)
        res = res.items[0].chat_settings
        response = [*res.admin_ids, res.owner_id]
        return response
        

    def isChatManager(self, from_id, peer_id: int):
        return from_id in self.getChatManagers(peer_id)


    async def getMembers(self, peer_id: int):
        response = await self.__api.messages.getConversationMembers(peer_id = peer_id)
        return [i.member_id for i in response.items]


    async def isMember(self, from_id: int, peer_id: int):
        return from_id in await self.getMembers(peer_id)


