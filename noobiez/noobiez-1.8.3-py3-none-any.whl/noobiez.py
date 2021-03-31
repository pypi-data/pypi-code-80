from .lic import Noobiez
from .connector import Connector
import threading,time,livejson,json

class Agz:

    class Core:
        def __init__(self, lic):
            self.lic = lic
            self.connector = Connector()

    class Storage:
        def __init__(self):
            self.user = {}
            self.chat = {}
            self.command = {
                "separator": " ",
                "prefix"   : ","
            }
            
    class User:

        def __init__(self, lic):
            self.lic = lic
          
        def __getitem__(self, mid):
            if mid not in self.lic.storage.user:
                self.lic.storage.user[mid] = {
                    "blacklist" : False,
                    "squad"     : False,
                    "osquad"     : False,
                    "permission": 0,
                    "war": False,
                    "ticket":None
                }
            return self.lic.storage.user[mid]
            

        def __iter__(self):
            return iter(self.lic.storage.user)

#######Status
    class Status:
    	def __init__(self):
    		self.status = {}
    class Setbot:
        def __init__(self, lic):
            self.lic = lic
            
        def __getitem__(self,mid):
        	if mid not in self.lic.bot.status:
        		self.lic.bot.status["status"] = {}
        	return self.lic.bot.status["status"]

        def __iter__(self):
            return iter(self.lic.bot.status)

######

#######Data
    class Data:
    	def __init__(self):
    		self.data = livejson.File("data.json")
    		self.protect = self.data["protect"]
    		self.master = self.data["master"]
    		self.ws = self.data["ws"]
    		self.skick = self.data["skick"]
    		self.cb = self.data["scb"]
    		self.byall = self.data["sbyall"]
    		self.respon = self.data["srp"]
    		self.invite = self.data["invite"]
    		
    		
    class Setting:
        def __init__(self, lic):
            self.lic = lic
            
        def __getitem__(self,mid):
        	if mid not in self.lic.data.protect+self.lic.data.master+self.lic.data.ws:
        		self.lic.data = {
        			"protect": {mid:False},
        			"ws": {mid:False},
        			"master": {mid:False},
        			"skick":{"STKVER":"","STKPKGID":"","STKID":0},
        			"scb":{"STKVER":"","STKPKGID":"","STKID":0},
        			"sbyall":{"STKVER":"","STKPKGID":"","STKID":0},
        			"invite":{"STKVER":"","STKPKGID":"","STKID":0},
        			"srp":{"STKVER":"","STKPKGID":"","STKID":0,"respon":""},
        		}
        	
        	return self.lic.data

        def __iter__(self):
            return iter(self.lic.data)

######


    class Chat:
        def __init__(self, lic):
            self.lic = lic

        def __getitem__(self, gid):
            if gid not in self.lic.storage.chat:
                self.lic.storage.chat[gid] = {
                    "squad": []
                }
            return self.lic.storage.chat[gid]

    class Command:
        def __init__(self, lic):
            self.lic = lic

        def __call__(self, string):
            splited = string.split(self.lic.storage.command["separator"])
            prefix = splited[0].lower()
            if prefix[:len(self.lic.storage.command["prefix"])] == self.lic.storage.command["prefix"]:
                arg = [prefix[len(self.lic.storage.command["prefix"]):]]
                if not arg[0]: arg = []
                args = arg + splited[1:]
                return args[0], args[1:]
            return False, []

    class Messenger:
        MAX_CACHE = 1000

        def __init__(self):
            self.cache = []
            self.lock = threading.Lock()

        def __call__(self, op, *key):
            key = "&".join(map(str, (op.createdTime if op.type not in [25, 26] else op.message.id,) + key))
            with self.lock:
                if key in self.cache:
                    return False
                self.cache.append(key)
                if len(self.cache) > self.MAX_CACHE:
                    self.cache = self.cache[self.MAX_CACHE//2]
                return True

    def __init__(self):
        self.storage = Agz.Storage()
        self.bot = Agz.Status()
        self.data = Agz.Data()
        self.core = Agz.Core(self)
        self.user = Agz.User(self)
        self.chat = Agz.Chat(self)
        self.command = Agz.Command(self)
        self.messenger = Agz.Messenger()
        self.status = Agz.Setbot(self)
        self.protect = Agz.Setting(self)
        self.ws = Agz.Setting(self)
        self.master = Agz.Setting(self)
        
        self.skick = Agz.Setting(self)
        self.cb = Agz.Setting(self)
        self.byall = Agz.Setting(self)
        self.respon = Agz.Setting(self)
        self.invite = Agz.Setting(self)
    

    def Noobiez(self, client,sockaddr,file):
        return Noobiez(self, client,sockaddr,file)



    