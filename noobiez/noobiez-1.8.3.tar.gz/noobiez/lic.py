from queue import Queue
import threading
import time, os, sys, livejson, json, ast
import socket
import random
import subprocess,platform,concurrent.futures
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser

###new get token####
from typing import Callable, Dict, Any
from lesting.api.client import build
class LoginResult:
	certificate: str
	accessToken: str
	lastBindTimestamp: int
	metaData: Dict[str, str]
HOST = "https://legy-jp.line.naver.jp"
PATH = HOST + "/acct/lgn/sq/v1"
POLL = HOST + "/acct/lp/lgn/sq/v1"
HEADERS = {"lite": {"user-agent": "LLA/2.16.0","x-line-apptrobosation": "ANDROIDLITE\t2.16.0\tAndroid OS\t10;SECONDARY"}}    
pclient = build("line.login", "v1")

Token= []
def getRequest(method: str, headers: Dict[str, str], *, lp: bool = False, **kwargs: Dict[str, Any]) -> Any:
	return getattr(pclient.parser, method)((pclient.http.request((POLL if lp else PATH), "POST", getattr(pclient.packer, method)(**kwargs), headers)[1]))
def loginWithQrCode(apptrobosation: str, certificate: str = "", web: bool = False, callback: Callable = lambda output: Token.append("{}".format(output))) -> LoginResult:
	headers = HEADERS[apptrobosation]
	session = getRequest("createSession", headers)
	result = getRequest("createQrCode", headers, session = session)
	callback(result.url)
	if web:
		callback(result.web)
	getRequest("checkQrCodeVerified", {**headers, **{"x-line-access": session}}, lp = True, session = session)
	try:
		getRequest("verifyCertificate", headers, session = session, certificate = certificate)
	except:
		pin = getRequest("createPinCode", headers, session = session)
		if web:
			pclient.pin.update(session, pin)
		else:
			callback(pin)
		getRequest("checkPinCodeVerified", {**headers, **{"x-line-access": session}}, lp = True, session = session)
	return getRequest("qrCodeLogin", headers, session = session, systemName = headers["x-line-apptrobosation"].split("\t")[2], autoLoginIsRequired = True) 

class Noobiez:
    def __init__(self, trobos, client, sockaddr,file):
        self.trobos = trobos
        self.client = client
        self.operations = Queue()
        self.running = False
        self.set = livejson.File("data.json")
        self.ser = livejson.File("lop.json")
        self.team = self.ser["team"]
        self.numSquad = self.ser["token"]
        self.master = self.set["master"]
        self.G_ticket = self.set["G_ticket"]
        self.protect = self.trobos.data.protect
        self.ws = self.trobos.data.ws
        self.mid = self.client.profile.mid
        self.wartTime = round(time.time())
        self.resend = {}
        self.loger = []
        self.online = True
        self.CMD = {"keyCommand":""}
        self.makers = ["u5f5ed5ad97bbf907f70a222ca9bc8de8","u76d9dc7ba456668e75595396323679f1"]
        self.upgradeSc = {"status":False,"group":None,"local":""}
        self.sockaddr = sockaddr
        self.file = str(file)
        #
        
        # send username
        
        self.queues = {}
        self.beckupQr = self.set["turbo"]
        self.Fast = self.set["fast"]
        self.force = self.set["force"]
        if self.set["squad"] != {}:
        	self.Squad = {mid for mid in self.set["squad"] if mid not in self.client.profile.mid}
        else:self.Squad = {}
        self.war = {}
        self.countWar = self.set["count"]["war"]
        if 0 == self.set["count"]["runtime"]:
        	self.set["count"]["runtime"] += time.time()
        self.starting = self.set["count"]["runtime"]
        
        self.client.count["kick"] += self.set["count"]["kick"]
        self.client.count["cancel"] += self.set["count"]["cancel"]
        self.client.count["invite"] += self.set["count"]["invite"]
        self.client.count["msg"] += self.set["count"]["msg"]
        self.upfoto = False
        self.Gmid = ""
        if self.set["steal"]["logo"] == "":
        	self.logo = self.client.logo
        else:
        	self.logo = self.set["steal"]["logo"]
        	self.client.logo = self.logo
        if self.set["steal"]["prefix"] != "":
        	self.trobos.storage.command["prefix"] = self.set["steal"]["prefix"]
        if self.mid in self.set["count"]["duedate"]:
        	if self.set["count"]["duedate"][self.mid] == "":
        		self.duedate = parser.parse(str(datetime.now()))
        	else:
        		self.duedate = parser.parse(str(self.set["count"]["duedate"][self.mid]))
        		self.client.limit = True
        else:
        	self.set["count"]["duedate"][self.mid] = ""
        	self.duedate = parser.parse(str(datetime.now()))
        	#time.sleep(1);self.sock.sendall(str({"func":"starting","userBots":self.mid,"status":self.client.limit}).encode("utf-8"))
        self.covid =""".1.2.3.4.5.6.7.8.9.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.

 Hello!
3xploi7 BuG
.1.2.3.4.5.6.7.8.9.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J. Hello!
3xploi7 BuG
.1.2.3.4.5.6.7.8.9.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.1.B.2.D.3.E.4.F.5.G.6.H.7.I.8.J.9.K.0.A.
"""
        self.promo = """╭◤ RENTAL WAR/PROTECT ◥
│• 6bot = R̶p̶.̶4̶0̶0̶K̶ (300K/MONTH)
│• 9bot = R̶p̶.̶6̶0̶0̶K̶ (500K/MONTH)
│• 12bot = R̶p̶.̶7̶5̶0̶K̶(600K/MONTH) 
│
│NB :
│  𝗕𝗢𝗧 𝗧𝗜𝗗𝗔𝗞 𝗠𝗨𝗗𝗔𝗛 𝗟𝗜𝗠𝗜𝗧/
│  𝗕𝗔𝗡𝗖𝗛𝗔𝗧
│  𝗝𝗘𝗡𝗜𝗦 𝗕𝗢𝗧 𝗖𝗟 (python++)
│  𝗗𝗔𝗡 𝗠𝗘𝗡𝗚𝗚𝗨𝗡𝗔𝗞𝗔𝗡 𝗦𝗬𝗦𝗧𝗘𝗠
│  𝗦𝗘𝗥𝗩𝗘𝗥 𝗧𝗖𝗣/𝗨𝗗𝗣
│  𝗕𝗢𝗧 𝗧𝗜𝗗𝗔𝗞 𝗡𝗚𝗘𝗕𝗨𝗚 (𝗶𝗻𝘃𝗶𝘁𝗲/𝗷𝗼𝗶𝗻)
│  𝗦𝗬𝗦𝗧𝗘𝗠 𝗕𝗔𝗖𝗞𝗨𝗣 𝗥𝗔𝗣𝗜𝗛 𝗗𝗔𝗡
│  𝗧𝗘𝗥𝗔𝗧𝗨𝗥
│  𝗕𝗢𝗧 𝗦𝗨𝗗𝗔𝗛 𝗠𝗘𝗡𝗚𝗚𝗨𝗡𝗔𝗞𝗔𝗡
│  - kick by replay (text/sticker)
│  - respon by sticker
│  - leaveall by sticker
│  - DLL
│
│𝗪𝗔𝗥𝗡𝗜𝗡𝗚
│  ᴊᴇɴɪꜱ ʙᴏᴛ ᴛɪᴅᴀᴋ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ
│  ꜱʏꜱᴛᴇᴍ ᴊꜱ,
│  ᴘᴜʀɢᴇ , ᴋɪᴄᴋ_ʙʟ, ʙʟ_ᴋᴀʀᴜɴɢᴀɴ
│  ᴅᴀɴ ꜱᴇᴊᴇɴɪꜱɴʏᴀ..
├──────────────
│payment
│• Paypal
│• Bank Indonesia
│
│contact us personally
│
│link ID: 
├「https://line.me/ti/p/rvoFBnRo76
╰ ◣ {logo} ◢""".format(logo=self.logo)
    def helpMessage(self,sender):
    	return """╭ ◤ 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦 ◥
│ 𝐮𝐬𝐞𝐫 : {user}
│ 𝐛𝐨𝐭𝐬 𝐜𝐨𝐮𝐧𝐭 : {count}/squad
│ 𝐬𝐪𝐮𝐚𝐝 𝐧𝐮𝐦𝐛 : {numSquad}
│ 𝐬𝐲𝐬𝐧𝐚𝐦𝐞  : {file}
│ 𝐯𝐞𝐫𝐬𝐢𝐨𝐧 : 𝐛𝐞𝐭𝐚 1.8.3 ex cPY++
│ 𝐚𝐜𝐜𝐨𝐦𝐩𝐚𝐧𝐢𝐞𝐝 𝐛𝐲 𝐭𝐡𝐞 𝐩𝐫𝐞𝐟𝐢𝐱 「 {pref} 」
├「 𝐆𝐄𝐍𝐄𝐑𝐀𝐋 」
│▸ help
│▸ cb
│▸ join
│▸ kick @target
│▸ invite
│▸ sp
│▸ say> (you text)
│▸ sname
├「 𝐆𝐑𝐎𝐔𝐏𝐒 」
│▸ groups
│▸ gurl (number group)
│▸ f*ck (for kickall)
│▸ link
│▸ ws
│▸ getme
│▸ bye
│▸ out
│▸ stay (count)
│▸ leftallgroup
│▸ http:(link group)
│▸ sentil (kick by replay)
│▸ sendcovid (number group)
│▸ gas (number group)
│▸ covid
│▸ nuke (number group)
├「 𝐒𝐄𝐓𝐓𝐈𝐍𝐆𝐒 」
│▸ set scb (Reply sticker)
│▸ set srp :(text) (Reply sticker)
│▸ set sbyeall (Reply sticker)
│▸ set skick (Reply sticker)
│▸ upsymbol: (text)
│▸ upprefix (symbol)
│▸ putsquad (token)
│▸ fix
│▸ update
│▸ upgrade (maker only)
│▸ owner @target
│▸ expel @target
├「 𝐒𝐄𝐓𝐁𝐎𝐓 」
│▸ bots
│▸ restart
│▸ cek
│▸ cekall
│▸ upname: (text)
│▸ here
│▸ rcount
│▸ count
│▸ cbots
│▸ rchat
│▸ mode low/smoth/ultra/god
│▸ sys
│▸ mytoken
│▸ uppict
│▸ log
│▸ logqr
├「 𝐏𝐑𝐎𝐓𝐄𝐂𝐓 」
│▸ pronull
│▸ promax
│▸ exec>(↰)(code)
├「 𝐌𝐄𝐃𝐈𝐀 」
│▸ tagall
╰ ◣ {logo} ◢""".format(numSquad=self.numSquad,file=self.file,pref=self.trobos.storage.command["prefix"],logo=self.logo,count=len(self.set["force"]),user=self.client.getContact(sender).displayName)
        
    def putBot(self):
    	try:
    		for s in self.set["squad"]:
    			self.trobos.user[s]["squad"] = True
    	except:
    		return
    
    def datas(self):
    	users = {mid: self.trobos.user[mid] for mid in self.trobos.user}
    	bots = {mid for mid, user in users.items() if user["squad"]}
    	pro = {gid for gid in self.trobos.data.protect}
    	self.sock.sendall(str({"cmd":"datas","datas": {"bots":bots,"pro":pro}, "To": "all"}).encode("utf-8"))

    def updateToken(self,mid):
    	time.sleep(3)
    	with open("token/{}.txt".format(self.file), "r") as f:
        	tlist = f.readlines()
        	squad = [x.strip() for x in tlist]
        	self.sock.sendall(str({"func":"uptok","squad":squad}).encode("utf-8"))


    def TCP(self):
    	try:
    		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    		threading.Thread(target=self.updateToken,args=(self.mid,)).start() 
    		self.sock.connect(self.sockaddr)
    		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    		self.username = self.mid
    		name = ""
    		for a in self.team:
    			name = a
    		self.sock.sendall(str({self.username:{self.file:name}}).encode("utf-8"))
    		rlist = [self.sock, sys.stdin]
    		print("TCP terhubung....")
    		while True:
    			self.recive()
    	except Exception as e:
    		if self.war:
    			pass
    		else:
    			if str(e) in ['[Errno 104] Connection reset by peer','[Errno 32] Broken pipe','[Errno 111] Connection refused']:
    				self.Restart()
        		
           

    def addWarTime(self):
    	self.wartTime = round(time.time()) + 1
    	return
    
    def Msg(self,op):
    		if op.type in [133,126]:terkick = op.param3
    		else:terkick = None
    		healty = self.client.limit
    		dataOp = {"createdTime":str(op.createdTime)}
    		blacklist = self.listBL()
    		notif = op.type
    		midBot = self.client.profile.mid
    		data = {"func":"queue","To":midBot,"op":dataOp,"blacklist":blacklist,"status":healty,"terkick":terkick,"type":notif}
    		self.sock.sendall(str(data).encode("utf-8"))
    		hasil = self.cekQueue(str(op.createdTime))
    		self.queues = {}
    		return hasil

    def cekQueue(self,createdTime):
    	num = 0
    	while True:
    		time.sleep(0.001)
    		if num <= 300:
    			if createdTime in self.queues:
    				return self.queues[createdTime]
    		else:
    			return True
    		num += 1
    		continue

    		


    def update(self,to):
    	self.sock.sendall(str({"func":"update","userBots":self.client.profile.mid,"group":to,"file":self.file}).encode("utf-8"))
    def upgradeFile(self,name,folder):
        self.sock.sendall(str({"func":"upgrade","userBots":self.client.profile.mid,"filename":name,"local":folder}).encode("utf-8"))
    def clearban(self,bot,to):
    	self.sock.sendall(str({"func":"clearban","group":to,"bot":bot}).encode("utf-8"))

    def restarting(self,bot,to):
    	self.sock.sendall(str({"func":"restarting","group":to,"bot":bot}).encode("utf-8"))
    	
    def banUser(self,user):
    	if user not in self.force and user not in self.master:self.trobos.user[user]["blacklist"] = True


    def recive(self):
        if self.upgradeSc["status"] == True:
        	with open(self.upgradeSc["local"], 'wb') as file:
        		while True:
        			data = self.sock.recv(1024)
        			print("start recive file")
        			if not data:
        				file.close()
        				print("saving data...")
        				self.client.sendMessage(self.upgradeSc["group"],"Result update For target_file: {}\nSystem upgrade Succsesfuly..".format(self.upgradeSc["local"]))
        				self.upgradeSc["status"] = False
        				self.Restart()
        				break
        			file.write(data)
        			continue
        reciv = self.sock.recv(2048).decode("utf-8")
        try:payload = ast.literal_eval(reciv)
        except:
        	return
        data = payload
        cmd = data["func"]
        
        ### for execution per bot

        if cmd == "upgrade":
        	self.upgradeSc["status"] = True
        	self.upgradeSc["local"] = data["local"]
        	return
        elif cmd == "crun":
        	squadnum = data["squad"]
        	usbot = data["usbot"]
        	to = data["group"]
        	with open("token/{}.txt".format(str(self.file)), "r") as f:
        		tlist = f.readlines()
        		squad = [x.strip() for x in tlist]
        		s = len(squad)
        		s -=1
        	if squadnum <= s:
        		lop = livejson.File("lop.json")
        		lop["token"] = squadnum
        		for b in self.set["squad"]:self.trobos.user[b]["squad"] = False
        		self.set["count"]["war"] = 0
        		self.set["squad"].clear()
        		if usbot == self.mid:self.client.sendMessage(to,"change squad {} success...".format(squadnum))
        		
        	else:self.client.sendMessage(to,"You squad just 0 - {}".format(s))
        	self.Restart()
        elif cmd == "mode":
        	mode = data["mode"]
        	usbot = data["usbot"]
        	to = data["group"]
        	if "low" == mode:
        		self.set["turbo"] = False
        		self.set["fast"] = False
        		if usbot == self.mid:self.client.sendMessage(to,"change to the lowest excecution system")
        		self.Restart()
        	if "smoth" == mode:
        		self.set["turbo"] = True
        		self.set["fast"] = False
        		if usbot == self.mid: self.client.sendMessage(to,"change to smoth excecution system")
        		self.Restart()
        	if "ultra" == mode:
        		self.set["turbo"] = False
        		self.set["fast"] = True
        		if usbot == self.mid:self.client.sendMessage(to,"change to ultra excecution system")
        		self.Restart()
        	if "god" == mode:
        		self.set["turbo"] = True
        		self.set["fast"] = True
        		if usbot == self.mid:self.client.sendMessage(to,"change to Highest execution system")
        		self.Restart()
        elif cmd == "resp":
        	if data["group"] in self.client.getAllChatMids(True).memberChatMids:
        		to = data["group"]
        		self.client.sendMessage(to,self.file)
        		return
        elif cmd == "ticket":
        	G_ticket = data["ticket"]
        	bot = data["bot"]
        	to = data["group"]
        	self.G_ticket = G_ticket
        	self.set["G_ticket"] = self.G_ticket
        	if bot == self.mid:
        		self.client.sendMessage(to,"update ticket {} group Success....".format(len(self.G_ticket)))
        	return
        elif cmd == "addtoken":
        	token = data["token"]
        	bot = data["bot"]
        	group = data["group"]
        	with open("token/{}.txt".format(self.file), "r") as f:
        		tlist = f.readlines()
        		squad = [x.strip() for x in tlist]
        	with open('token/{}.txt'.format(self.file), 'a') as c:
        		if token not in squad:
        			c.write("\n{}".format(token))
        	if bot == self.mid:
        		self.client.sendMessage(group,"share token sukses...")
        elif cmd == "addtokenFailed":
        	group = data["group"]
        	kembar = "Token ini sudah ada\n\n"
        	for k in data["kembar"]:
        		kembar += "{}\n".format(k)
        	self.client.sendMessage(group,kembar)
        elif cmd == "queue":
        	try:
        		hasil = data["hasil"]
        		timer = data["Time"]
        		blacklist = data["blacklist"]
        		if blacklist != []:
        			for bl in blacklist:threading.Thread(target=self.banUser,args=(bl,)).start()
        		self.queues = {timer:hasil}
        		return
        	except Exception as e:print(str(e))
        elif cmd == "restarting":
        	bot = data["bot"]
        	to = data["group"]
        	if bot == self.mid:self.client.sendMessage(to,"System restart....")
        	self.Restart()
        elif cmd == "restart":
        	self.Restart()
        elif cmd == "resys":
        	team = data["team"]
        	port = data["port"]
        	print("Please Save you name team for next login another bots [ {} ]".format(team))
        	self.ser["team"][team] = int(port)
        	self.Restart()
        elif cmd == "gaskeun":
        	mem = data["mem"]
        	pen = data["pen"]
        	to = data["group"]
        	self.war[to] = True
        	self.Ulty(to,mem,pen)
        	return
        elif cmd == "staySquad":
        	try:
        		squad = data["bots"]
        		for b in self.force:
        			if b in squad:
        				if b not in self.set["squad"]:
        					if b not in data["limit"]:
        						self.trobos.user[b]["squad"] = True
        						self.set["squad"][b] = True
        				else:self.trobos.user[b]["squad"] = True
        			else:
        				if b in self.set["squad"]:
        					self.trobos.user[b]["squad"] = False
        					del self.set["squad"][b]
        				else:self.trobos.user[b]["squad"] = False
        		if self.client.profile.mid in self.set["squad"]:
        			to = data["group"]
        			group = to
        			t = data["ticket"]
        			ticket = t
        			try:self.client.acceptChatInvitationByTicket(to,ticket)
        			except Exception as e:
        				if 'code=35' in str(e):
        					self.client.limit = True
        		self.Squad = {mid for mid in squad if mid not in self.mid}
        	except:pass
        elif cmd == "stayBots":
        	try:
        		squad = data["bots"]
        		for b in self.force:
        			if b in squad:
        				if b not in self.set["squad"]:
        					if b not in data["limit"]:
        						self.trobos.user[b]["squad"] = True
        						self.set["squad"][b] = True
        				else:self.trobos.user[b]["squad"] = True
        			else:
        				if b in self.set["squad"]:
        					self.trobos.user[b]["squad"] = False
        					del self.set["squad"][b]
        				else:self.trobos.user[b]["squad"] = False
        		if self.client.profile.mid == data["capten"]:
        			time.sleep(0.2)
        			self.cekQr(data["group"])
        			if data["limit"] != []:
        				self.client.sendMentionWithList(data["group"], "BAD REQUEST",data["limit"])
        		if self.client.profile.mid not in self.set["squad"]:
        			self.client.deleteSelfFromChat(data["group"])
        		self.Squad = {mid for mid in squad if mid not in self.mid}
        	except:pass
        ### for all bots
        elif cmd == "join":
        	if self.trobos.user[self.mid]["squad"]:
        		if data["group"] not in self.client.getAllChatMids(True).memberChatMids:
        			to = data["group"]
        			group = to
        			t = data["ticket"]
        			ticket = t
        			try:self.client.acceptChatInvitationByTicket(to,ticket)
        			except Exception as e:
        				if 'code=35' in str(e):
        					self.client.limit = True
        elif cmd == "bqr":
        	if self.trobos.user[self.mid]["squad"]:
        		if data["group"] not in self.client.getAllChatMids(True).memberChatMids:
        			to = data["group"]
        			group = to
        			t = data["ticket"]
        			ticket = t
        			try:
        				self.client.acceptChatInvitationByTicket(group,ticket)
        				count = [mid for mid in self.trobos.user if self.trobos.user[mid]["blacklist"]]
        				self.killModeqr(group,count)
        				return
        			except Exception as e:
        				if 'code=35' in str(e):
        					self.client.limit = True
        				elif 'code=5' in str(e):
        					return
        			return
        elif cmd == "datas":
        	for b in data["bots"]:
        		self.trobos.user[b]["squad"] = True
        	for p in data["pro"]:
        		if p not in self.trobos.data.protect:
        			self.trobos.data.protect[p] = True
        	return
        elif cmd == "update":
        	for mid in data["bots"]["squad"]:
        		self.trobos.user[mid]["squad"] = True
        		self.set["squad"][mid] = True
        		self.set["force"] = data["bots"]["squad"]
        	self.Squad = {mid for mid in data["bots"]["squad"] if mid not in self.mid}
        	self.client.sendMessage(data["bots"]["group"],"success updating...")
        elif cmd == "clearban":
        	to = data["group"]
        	bot = data["bot"]
        	users = [self.trobos.user[mid] for mid in self.trobos.user if self.trobos.user[mid]["blacklist"]]
        	list = [mid for mid in self.trobos.user if self.trobos.user[mid]["blacklist"]]
        	if list != []:
        		self.war[to] = False
        		tx = "Clear {} users Blackist".format(len(list))
        		if bot == self.mid:self.client.sendMentionWithList(to,tx,list )
        		for user in users:user["blacklist"] = False
        	else:
        		if bot == self.mid:self.client.sendMessage(to,"Not have users Blacklist	╮(╯▽╰)╭")
        	self.Restart()
        	return
        elif cmd == "reqstat":
        	try:
        		self.client.deleteOtherFromChat(self.mid,{self.mid})
        	except Exception as e:
        		if 'code=35' in str(e):
        			if self.set["count"]["duedate"][self.mid] == "":
        				self.duedate = self.duedate + relativedelta(hours= -1)
        				self.set["count"]["duedate"][self.mid] = str(self.duedate)
        				self.client.limit = True
        		elif 'code=20' in str(e):
        			if self.set["count"]["duedate"][self.mid] == "":
        				self.duedate = self.duedate + relativedelta(hours= 1)
        				self.set["count"]["duedate"][self.mid] = str(self.duedate)
        				self.client.limit = True
        		elif 'code=0' in str(e):
        			self.set["count"]["duedate"][self.mid] = ""
        	self.sock.sendall(str({"func":"getstat","duedate":self.set["count"]["duedate"][self.mid],"bot":self.mid}).encode("utf-8"))
        	return
        elif cmd == "getstat":
        	to = data["group"]
        	statdata = data["data"]
        	good = []
        	bad = []
        	for b in statdata:
        		if statdata[b] == "":
        			good.append(b)
        		else:
        			bad.append(b)
        	tx = "╭ ◤ 𝐁𝐎𝐓𝐒 𝐒𝐓𝐀𝐓𝐔𝐒 ◥\n"
        	tx += "│\n"
        	if good != []:
        		tx += "│𝚁𝙴𝚀𝚄𝙴𝚂𝚃 GOOD\n"
        		numG = 0
        		for g in good:
        			numG += 1
        			tx += "│{}.{}\n".format(numG,self.client.getContact(g).displayName)
        	tx += "│\n"
        	if bad != []:
        		tx += "│𝚁𝙴𝚀𝚄𝙴𝚂𝚃 BAD\n"
        		numB = 0
        		for x in bad:
        			numB += 1
        			self.duedate = parser.parse(str(statdata[x]))
        			timeleft = self.duedate - datetime.now()
        			days, seconds = timeleft.days, timeleft.seconds
        			hours = seconds / 3600
        			minutes = (seconds / 60) % 60
        			tx += "│{}.{}\n│ 		𝐭𝐢𝐦𝐞𝐥𝐞𝐟𝐭: {}:{}\n".format(numB,self.client.getContact(x).displayName,round(hours),round(minutes))
        	tx += "╰ ◣ {} ◢".format(self.logo)
        	self.client.sendMessage(to,tx)
        		
        					
    def fetch(self):
        #with concurrent.futures.ThreadPoolExecutor(max_workers=5) as workOp:
        	while True:
        		self.startup = round(time.time() * 1000)
        		self.running = False
        		time.sleep(5)
        		self.putBot()
        		while True:
        			ops = self.client.realFetchOps()
        			for op in ops:
        				if not self.running:
        					if op.createdTime < self.startup:
        						continue
        					self.running = True
        				self.operations.put(op) #workOp.submit(self.operations.put,op)

    def executor(self):
    	while True:
    		try:
    			self.execute(self.operations.get()) #with concurrent.futures.ThreadPoolExecutor() as workOp:workOp.submit(self.execute,self.operations.get())
    		except:
    			import traceback
    			traceback.print_exc()

    def detectBot(self,to):
    	chat = self.client.chats[to]
    	users = {mid: self.trobos.user[mid] for mid in self.trobos.user}
    	bots = {mid for mid, user in users.items() if user["squad"] and mid not in chat.members and mid not in chat.invites and mid not in self.mid} #chat.members and mid not in chat.invites and mid not in 
    	return bots

    def stayBot(self,to):
    	chat = self.client.getChat(to).extra.groupExtra #.memberMids or .inviteeMids
    	users = {mid: self.trobos.user[mid] for mid in self.trobos.user}
    	bots = {mid for mid, user in users.items() if user["squad"] if mid in chat.memberMids} #chat.members and mid not in chat.invites and mid not in 
    	return bots

    def notAllow(self,user):
    	if user not in self.master and user not in self.force:
    		return True
    	return False

    def alowed(self,user):
    	try:
    		param2 = self.trobos.user[user]
    		if param2["squad"] or user in self.master:
    			return True
    		return False
    	except:
    		return False
    def proGroup(self,op):
    	to = op.param1
    	user = op.param2
    	try:
    		if to in self.trobos.data.protect:
    			if self.trobos.data.protect[to] == True:
    				if self.alowed(user):
    					return False
    				return True
    		return False
    	except:
    		return False
    def warGroup(self,to):
    	if to in self.war:
    		return True
    	return False
    
    def lockQr(self,to):
    	D = self.client.getChat(to)
    	D.extra.groupExtra.preventedJoinByTicket = True
    	self.client.updateChat(D,4)
    	return
    	
    def cekQr(self,to):
    	D = self.client.getChat(to)
    	qr = D.extra.groupExtra.preventedJoinByTicket
    	if qr == False:
    		D.extra.groupExtra.preventedJoinByTicket = True
    		self.client.updateChat(D,4)
    	return

    def joinQr(self,to):
    	time.sleep(0.004)
    	D = self.client.getChat(to)
    	qr = D.extra.groupExtra.preventedJoinByTicket
    	if qr == True:
    		D.extra.groupExtra.preventedJoinByTicket = False
    	self.client.updateChat(D,4)
    	ticket = self.client.reissueChatTicket(to)
    	self.sock.sendall(str({"func":"join","To":"all","ticket":ticket,"group":to}).encode("utf-8"))
    	def lock():
    		users = {mid: self.trobos.user[mid] for mid in self.trobos.user}
    		bots = {mid for mid, user in users.items() if user["squad"]}
    		if len(self.detectBot(to)) <= len(bots):
    			time.sleep(0.02)
    			return self.cekQr(to)
    	lock()

    def forceJoin(self,to,count):
    	time.sleep(0.004)
    	if len(self.stayBot(to)) <= count:
    		D = self.client.getChat(to)
    		qr = D.extra.groupExtra.preventedJoinByTicket
    		if qr == True:
    			D.extra.groupExtra.preventedJoinByTicket = False
    		self.client.updateChat(D,4)
    	k = [mid for mid in self.stayBot(to)]
    	ticket = self.client.reissueChatTicket(to)
    	self.sock.sendall(str({"func":"forceJoin","userBots":self.mid,"ticket":ticket,"group":to,"count":count,"stay":k}).encode("utf-8"))
    	return

    def bqr(self,to):
    	D = self.client.getChat(to)
    	qr = D.extra.groupExtra.preventedJoinByTicket
    	if qr == True:
    		D.extra.groupExtra.preventedJoinByTicket = False
    		self.client.updateChat(D,4)
    	ticket = self.G_ticket[to]
    	self.sock.sendall(str({"func":"bqr","ticket":ticket,"group":to}).encode("utf-8"))

    def bqr2(self,to):
    	D = self.client.getChat(to)
    	qr = D.extra.groupExtra.preventedJoinByTicket
    	if qr == False:
    		ticket = self.G_ticket[to]
    		self.sock.sendall(str({"func":"bqr","ticket":ticket,"group":to}).encode("utf-8"))
 
    def accQr(self,to):
    	try:
    		gc = self.trobos.user[to]
    		if None != gc["ticket"]:
    			ticket = self.trobos.user[to]["ticket"]
    			gwar = self.client.chats[to].members
    			if self.client.profile.mid not in gwar:
    				self.client.acceptChatInvitationByTicket(to,ticket)
    				bots = {mid for mid, user in users.items() if user["squad"]}
    				for b in bots:
    					if b not in gwar:
    						return
    				self.trobos.user[to]["ticket"] = None
    			return
    		else:
    			time.sleep(0.2)
    			return self.accQr(to)
    	except:
    		self.trobos.user[to]["ticket"] = None
    		return

    def equal(self,to,target):
    	for x in target:
    		try:
    			if self.trobos.user[x]["blacklist"]:
    				return True
    		except:return False
    	return False

    def detectUser(self,user):
    	if user not in self.trobos.user:
    		self.trobos.user[user]["blacklist"] = False
    		self.trobos.user[user]["squad"] = False
    		return self.trobos.user[user]
    	return self.trobos.user[user]

    def detectUscont(self,user):
    	if user in self.master:
    		return True
    	return False
    	

    def listBL(self):
    	count = [mid for mid in self.trobos.user if self.trobos.user[mid]["blacklist"]]
    	return count

    def autoPurge(self):
    	
    	count = [mid for mid in self.trobos.user if self.trobos.user[mid]["blacklist"]]
    	if 2 <= len(count):
    		return True, count
    	return False, []
    def killMode(self,to,count):
    	#time.sleep(0.02)
    	chat = self.client.getChat(to).extra.groupExtra.memberMids
    	for b in count:
    		if b in chat:
    			threading.Thread(target=self.client.deleteOtherFromChat, args=(to, {b}, )).start() 
    def killModeqr(self,to,count):
    	#time.sleep(0.02)
    	chat = self.client.getChat(to).extra.groupExtra
    	for b in count:
    		if b in chat.memberMids:
    			threading.Thread(target=self.client.deleteOtherFromChat, args=(to, {b}, )).start()
    			continue
    		if b in chat.inviteeMids:threading.Thread(target=self.client.cancelChatInvitation, args=(to, b, )).start()
    			

    def realkillMode(self,to,count):
    	chat = self.client.chats[to]
    	for x in count:
    		if x in chat.members:
    			threading.Thread(target=self.client.deleteOtherFromChat, args=(to, {x}, )).start()

    def command(self,text):
    	pesan = text
    	if pesan.startswith(self.CMD["keyCommand"]):
    		cmd = pesan.replace(self.CMD["keyCommand"],"")
    		#self.CMD["allow"] = True
    	else:
    		cmd = "command"
    	return cmd

    def cfoto(self, token):
    	file = open("cf.py", "w")
    	file.write("from upfoto import *\nfrom datetime import datetime, timedelta\nimport time, random, sys, json, codecs, threading, asyncio, glob, re, string, os, six, ast, pytz, atexit, traceback,requests\npub = LINE('{}',appName='ANDROIDLITE	2.14.0	Android OS	10')\na = 'img.jpg'\ntry:pub.updateProfilePicture(a)\nexcept:pub.updateProfilePicture(a)".format(token))
    	file.close()
    	os.system('python3.6 cf.py')
    
    def sendUnicode(self,to):
    	t = self.client.sendMessage(to, self.covid)
    	time.sleep(1)
    	self.client.unsendMessage(t.id)
    	jem = self.client.sendMessage(to, "mid")
    	time.sleep(1)
    	self.client.unsendMessage(jem.id)
    
    def countdownTimer(self,start_minute, start_second):
    	total_second = int(start_minute) * 60 + int(start_second)
    	while total_second:
    		mins, secs = divmod(total_second, 60)
    		print(f'{mins:02d}:{secs:02d}', end='\r')
    		time.sleep(1)
    		total_second -= 1
    		self.war = {}
    def Ulty(self,to,mem,pen):
        cmd = 'node ulty.js token={} gid={}'.format(self.client.authToken, to)
        for uid in mem:
        	cmd += ' uid={}'.format(uid)
        	self.trobos.user[uid]["blacklist"] = True
        for cud in pen:
        	cmd += ' cud={}'.format(cud)
        	self.trobos.user[cud]["blacklist"] = True
        os.system(cmd)
        return
    def cclBLp(self,to,invite):
        for cud in invite:
        	if self.trobos.user[cud]["blacklist"]:threading.Thread(target=self.client.cancelChatInvitation, args=(to, cud, )).start()

    def kickBL(self,to):
    	list = [mid for mid in self.trobos.user if self.trobos.user[mid]["blacklist"]]
    	chat = self.client.getChat(to).extra.groupExtra
    	for b in list:
    		if b in chat.memberMids:
    			threading.Thread(target=self.client.deleteOtherFromChat, args=(to, {b}, )).start()
    			continue
    		if b in chat.inviteeMids:threading.Thread(target=self.client.cancelChatInvitation, args=(to, b, )).start()
    def Restart(self):
    	self.set["count"]["kick"] = self.client.count["kick"]
    	self.set["count"]["cancel"] =self.client.count["cancel"]
    	self.set["count"]["invite"] =self.client.count["invite"]
    	self.set["count"]["msg"] =self.client.count["msg"]
    	self.set["count"]["runtime"] = self.starting
    	list = [mid for mid in self.trobos.user if self.trobos.user[mid]["blacklist"]]
    	if 4 <= len(list):self.set["count"]["war"] += 1
    	time.sleep(3)
    	python = sys.executable
    	os.execl(python, python, *sys.argv)



    def Restartall(self,to,op):
    	if self.Msg(op):
    		self.client.sendMessage(to, "Restart system...")

    def accGroup(self,op):
    	self.client.acceptChatInvitation(op.param1)
    	if op.param2 in self.master:
    		gcMid = self.client.getChat(op.param1).extra.groupExtra
    		bots = {mid for mid in self.Squad if mid not in gcMid.memberMids}
    		if bots:
    			for b in bots:
    				if b in gcMid.inviteeMids:self.client.cancelChatInvitation(op.param1, b)
    			try:self.client.inviteIntoChat(op.param1,bots)
    			except:self.joinQr(op.param1)
    		return

    def GasKeun(self,to): 
        					users = {mid: self.trobos.user[mid] for mid in self.trobos.user}
        					squad = {mid for mid, user in users.items() if user["squad"]}
        					group = self.client.getChat(to).extra.groupExtra
        					nobiez = {mid for mid in self.Squad if mid not in group.memberMids}
        					if nobiez:
        						self.joinQr(to)
        					bot = {}
        					s = []
        					for b in squad:
        						bot[b] = {"mem":[],"pen":[]}
        						s.append(b)
        					group = self.client.getChat(to).extra.groupExtra
        					mem = []
        					pen = []
        					target = []
        					
        					for i in group.memberMids:
        						if self.notAllow(i):
        							target.append(i)
        							mem.append(i)
        					for q in group.inviteeMids:
        						if self.notAllow(q):
        							target.append(q)
        							pen.append(q)
        					tx = "target total {} :m>{} p>{}\n".format(len(target),len(mem),len(pen))
        					def exemple(t,b,e,mem,pen):
        						tar = t
        						bo = b
        						j = e
        						for a in j:
        							if tar:
        								x = random.choice(tar)
        								if x in mem:
        									bo[a]["mem"].append(x)
        								if x in pen:
        									bo[a]["pen"].append(x)
        								t.remove(x)
        							else:
        								return bo
        						if tar:
        							return exemple(tar,bo,j,mem,pen)
        						else:
        							return bo
        					bots = exemple(target,bot,s,mem,pen)
        					for u in bots:
        						self.sock.sendall(str({"func":"gaskeun","data":bots[u],"group":to,"for":u}).encode("utf-8"))
        						print("send > {}".format(u))
        					for a in bots:
        						tx += "bot {} dapet k>{} c>{}\n".format(self.client.getContact(a).displayName,		len(bots[a]["mem"]),	len(bots[a]["pen"]))
        					return tx
    def execute(self,op):
        try:
        	if op.type in [13, 124]:
        		param2 = self.detectUser(op.param2)
        		invite = op.param3.split("\x1e")
        		if self.client.profile.mid in invite:
        			threading.Thread(target=self.accGroup, args=(op, )).start()
        			return
        		if param2["squad"] or op.param2 in self.master:return
        		if self.equal(op.param1,invite):
        			param2["blacklist"] = True
        			if self.Msg(op):
        				for cud in invite:
        					if self.trobos.user[cud]["blacklist"]:
        						threading.Thread(target=self.client.cancelChatInvitation, args=(op.param1, cud, )).start()
        						continue
        					threading.Thread(target=self.client.deleteOtherFromChat, args=(op.param1, {cud}, )).start()
        					self.trobos.user[cud]["blacklist"] = True
        				threading.Thread(target=self.client.deleteOtherFromChat, args=(op.param1, {op.param2}, )).start()
        				return
        		else:
        			if op.param1 in self.war:return
        			if self.proGroup(op):
        				for bl in invite:threading.Thread(target=self.client.cancelChatInvitation, args=(op.param1, bl, )).start();self.trobos.user[bl]["blacklist"] = True
        				param2["blacklist"] = True
        				threading.Thread(target=self.client.deleteOtherFromChat, args=(op.param1, {op.param2}, )).start()

        	elif op.type in [11, 122]:
        		param2 = self.detectUser(op.param2)
        		if param2["squad"]:return
        		if op.param2 in self.master:return
        		if self.warGroup(op.param1):
        			param2["blacklist"] = True
        			if self.Msg(op):
        				if self.beckupQr:threading.Thread(target=self.bqr, args=(op.param1,)).start()
        				else:threading.Thread(target=self.lockQr, args=(op.param1,)).start()
        				cecking ,count= self.autoPurge()
        				if cecking and self.Fast:self.killMode(op.param1,count)
        				else:threading.Thread(target=self.client.deleteOtherFromChat, args=(op.param1, {op.param2}, )).start()
        				return
        		else:
        			if op.param1 in self.war:return
        			if param2["squad"]:return
        			if self.proGroup(op):
        				if self.Msg(op):
        					threading.Thread(target=self.client.deleteOtherFromChat, args=(op.param1, {op.param2}, )).start()
        					threading.Thread(target=self.lockQr, args=(op.param1,)).start()

        	elif op.type in [17, 130]:
        		param2 = self.detectUser(op.param2)
        		invites = self.detectBot(op.param1)
        		if param2["squad"] or op.param2 in self.master or op.param2 in self.trobos.data.ws:return
        		if param2["blacklist"]:
        			if self.Msg(op):
        				if self.beckupQr:
        					cecking ,count= self.autoPurge()
        					if cecking and self.Fast:self.killMode(op.param1,count)
        					else:threading.Thread(target=self.client.deleteOtherFromChat, args=(op.param1, {op.param2}, )).start()
        					return
        				else:
        					threading.Thread(target=self.client.deleteOtherFromChat, args=(op.param1, {op.param2}, )).start()
        					threading.Thread(target=self.cekQr, args=(op.param1,)).start()
        					return
        		else:
        			if op.param1 in self.war:return
        			if self.proGroup(op):
        				if self.Msg(op):
        					threading.Thread(target=self.cekQr, args=(op.param1,)).start()
        					return
 

        	elif op.type in [19, 133]:
        		param2 = self.detectUser(op.param2)
        		param3 = self.detectUser(op.param3)
        		if param2["squad"] or op.param2 in self.master:return
        		if op.param3 == self.client.profile.mid:
        			param2["blacklist"] = True
        			return
        		if param3["squad"]:
        			param2["blacklist"] = True
        			self.war[op.param1] = True
        			if self.Msg(op):
        				cecking ,count= self.autoPurge()
        				if cecking and self.Fast:self.killMode(op.param1,count)
        				else:threading.Thread(target=self.client.deleteOtherFromChat, args=(op.param1, {op.param2}, )).start()
        				threading.Thread(target=self.client.inviteIntoChat, args=(op.param1, self.Squad, )).start()
        				if self.beckupQr:threading.Thread(target=self.bqr, args=(op.param1,)).start()
        				return
        			
        		else:
        			if op.param1 in self.war:return
        			if self.proGroup(op):
        				if self.Msg(op):
        					threading.Thread(target=self.client.deleteOtherFromChat, args=(op.param1, {op.param2}, )).start()
        					threading.Thread(target=self.client.findAndAddContactsByMid, args=(op.param3,)).start()
        					threading.Thread(target=self.client.inviteIntoChat, args=(op.param1, {op.param3}, )).start()
        					return
        			else:
        				if op.param3 in self.master:
        					param2["blacklist"] = True
        					if self.Msg(op):
        						threading.Thread(target=self.client.deleteOtherFromChat, args=(op.param1, {op.param2}, )).start()
        						threading.Thread(target=self.client.findAndAddContactsByMid, args=(op.param3,)).start()
        						threading.Thread(target=self.client.inviteIntoChat, args=(op.param1, {op.param3}, )).start()


        	elif op.type in [32, 126]:
        		param2 = self.detectUser(op.param2)
        		param3 = self.detectUser(op.param3)
        		if param2["squad"] or op.param2 in self.master:return
        		if op.param3 == self.client.profile.mid:param2["blacklist"] = True ;return
        		if param3["squad"]:
        			param2["blacklist"] = True
        			if self.Msg(op):
        				threading.Thread(target=self.client.deleteOtherFromChat, args=(op.param1, {op.param2}, )).start()
        				threading.Thread(target=self.client.inviteIntoChat, args=(op.param1, self.Squad, )).start()
        				if self.beckupQr:threading.Thread(target=self.bqr, args=(op.param1,)).start()
        				return
        		else:
        			if op.param1 in self.war:return
        			if self.proGroup(op):
        				if self.Msg(op):
        					threading.Thread(target=self.client.deleteOtherFromChat, args=(op.param1, {op.param2}, )).start()
        					threading.Thread(target=self.client.findAndAddContactsByMid, args=(op.param3,)).start()
        					threading.Thread(target=self.client.inviteIntoChat, args=(op.param1, {op.param3}, )).start()
        					return
        			else:
        				if op.param3 in self.master:
        					param2["blacklist"] = True
        					if self.Msg(op):
        						threading.Thread(target=self.client.deleteOtherFromChat, args=(op.param1, {op.param2}, )).start()
        						threading.Thread(target=self.client.findAndAddContactsByMid, args=(op.param3,)).start()
        						threading.Thread(target=self.client.inviteIntoChat, args=(op.param1, {op.param3}, )).start()

        				


        	elif op.type == 5:
        		if op.param1 in self.client.contacts:
        			return
        		else:
        			self.client.findAndAddContactsByMid(op.param1)
        			self.client.sendMessage(op.param1, "thanks for add\n"+self.promo)
        			return

        	elif op.type == 26:
        		msg = op.message
        		if 'MENTION' in msg.contentMetadata.keys() != None and self.client.profile.mid in [x["M"] for x in eval(msg.contentMetadata['MENTION'])["MENTIONEES"]]:
        			text = self.trobos.storage.command["prefix"]+msg.text[int(eval(msg.contentMetadata['MENTION'])["MENTIONEES"][-1]['E'])+1:].replace('\n','')
        		else:text = msg.text
        		msg_id = msg.id
        		receiver = msg.to
        		msg.from_ = msg._from
        		sender = msg._from
        		to = msg.to
        		

        		if msg._from in self.master:
        			if to in self.client.profile.mid:
        				print(msg.text[:5])
        				if "https" == str(msg.text[:5]):
        					gc = self.client.findChatByTicket(msg.text[23:]).chatMid
        					self.client.acceptChatInvitationByTicket(gc,msg.text[23:])


        		if msg.contentType == 7:
        			if msg._from in self.master:
        				if msg.contentMetadata["STKID"] in str(self.trobos.data.skick["STKID"]) and msg.contentMetadata["STKPKGID"] in self.trobos.data.skick["STKPKGID"] and msg.contentMetadata["STKVER"] in self.trobos.data.skick["STKVER"]:
        					if msg.relatedMessageId == None:return self.client.sendMessage(to, 'Reply Message not found.')
        					M = self.client.getRecentMessagesV2(to, 1001)
        					anu = []
        					for ind, i in enumerate(M):
        						if i.id == msg.relatedMessageId:
        							anu.append(i)
        					self.trobos.user[anu[0]._from]["blacklist"] = True
        					self.war[to] = True
        					if self.Msg(op):
        						time.sleep(1)
        						try:self.client.deleteOtherFromChat(to, {anu[0]._from});return
        						except:self.client.sendMessage(to, "Error 404")
        						return

        				if msg.contentMetadata["STKID"] in str(self.trobos.data.respon["STKID"])  and msg.contentMetadata["STKPKGID"] in self.trobos.data.respon["STKPKGID"] and msg.contentMetadata["STKVER"] in self.trobos.data.respon["STKVER"]:
        					self.client.sendMessage(to, self.trobos.data.respon["respon"])
        					return
        				if msg.contentMetadata["STKID"] in str(self.trobos.data.byall["STKID"]) and msg.contentMetadata["STKPKGID"] in self.trobos.data.byall["STKPKGID"] and msg.contentMetadata["STKVER"] in self.trobos.data.byall["STKVER"]:
        					self.client.deleteSelfFromChat(to)
        					return
        				if msg.contentMetadata["STKID"] in str(self.trobos.data.cb["STKID"]) and msg.contentMetadata["STKPKGID"] in self.trobos.data.cb["STKPKGID"] and msg.contentMetadata["STKVER"] in self.trobos.data.cb["STKVER"]:
        					if self.Msg(op):
        						self.clearban(self.mid,to)
        					if msg.contentMetadata["STKID"] in str(self.trobos.data.invite["STKID"]) and msg.contentMetadata["STKPKGID"] in self.trobos.data.invite["STKPKGID"] and msg.contentMetadata["STKVER"] in self.trobos.data.invite["STKVER"]:
        						self.joinQr(to)
        						return

        		if text is None:return
        		if msg._from not in self.master:return
        		
        		if msg.toType == 2:
        			if msg.contentType == 1:
        				if self.upfoto == True:
        					path = self.client.downloadMsg(msg_id, "img.jpg")
        					self.upfoto = False
        					self.cfoto(self.client.authToken)
        					self.client.sendMessage(to,'success Update photo profile...')
        		
        		cmds = self.command(text)
        		for jembot in range(len(cmds.split('\n'))):
        			comd = cmds.split('\n')[jembot]
        			if jembot != 0:
        				comd = self.trobos.storage.command["prefix"]+cmds.split('\n')[jembot]
        			command, args = self.trobos.command(comd)
        			if command == False:return
        			if command == "cb":
        				if self.Msg(op):
        					self.clearban(self.mid,to)

        			if command.startswith("kick"):
        				#if self.Msg(op):
        					MENTION = msg.contentMetadata.get("MENTION", None)
        					if MENTION:
        						chat = self.client.chats[to]
        						MENTIONEES = eval(MENTION)["MENTIONEES"]
        						self.war[to] = True
        						target = []
        						for mention in MENTIONEES:
        							if mention["M"] in chat.members:
        								self.trobos.user[mention["M"]]["blacklist"] = True
        								target.append(mention["M"])
        						if self.Msg(op):
        							time.sleep(1)
        							for monyet in target:
        								threading.Thread(target=self.client.deleteOtherFromChat, args=(to, {monyet}, )).start()

        			if command.startswith("owner"):
        				#if self.Msg(op):
        					MENTION = msg.contentMetadata.get("MENTION", None)
        					if MENTION:
        						chat = self.client.chats[to]
        						MENTIONEES = eval(MENTION)["MENTIONEES"]
        						for mention in MENTIONEES:
        							if mention["M"] in chat.members:
        								self.master[mention["M"]] = True
        								self.client.sendMessage(to,"Add to owner succses")

        			if command.startswith("bot"):
        				#if self.Msg(op):
        					MENTION = msg.contentMetadata.get("MENTION", None)
        					if MENTION:
        						chat = self.client.chats[to]
        						MENTIONEES = eval(MENTION)["MENTIONEES"]
        						for mention in MENTIONEES:
        							if mention["M"] in chat.members:
        								self.trobos.user[mention["M"]]["squad"] = True
        								self.client.sendMessage(to,"Add to bots succses")

        			if command.startswith("expel"):
        				#if self.Msg(op):
        					MENTION = msg.contentMetadata.get("MENTION", None)
        					if MENTION:
        						chat = self.client.chats[to]
        						MENTIONEES = eval(MENTION)["MENTIONEES"]
        						targets = []
        						for mention in MENTIONEES:
        							if mention["M"] in chat.members:
        								targets.append(mention["M"])
        						owner = []
        						for u in targets:
        							if u in self.master:owner.append(u);del self.set["master"][u]
        						if owner !=[]:self.client.sendMentionWithList(to,"expeld {} user from owner".format(len(owner)),owner )
        								
        			if command == "groups":
        				group = self.client.getAllChatMids(True).memberChatMids
        				tx ="╭ ◤ GROUP ◥\n"
        				num = 0
        				for g in group:
        					num +=1
        					tx += "│{}.{}│{}\n".format(num,self.client.getChat(g).chatName,len(self.client.getChat(g).extra.groupExtra.memberMids))
        				tx += "╰ ◣ {} ◢".format(self.logo)
        				self.client.sendMessage(to, tx)

        			if command.startswith("gurl"):
        				if self.Msg(op):
        					split = text.split(" ")
        					group = []
        					try:
        						for xx in self.client.getAllChatMids(True).memberChatMids:group.append(xx)
        						gc = group[int(split[1]) - 1]
        						D = self.client.getChat(gc)
        						if D.extra.groupExtra.preventedJoinByTicket == True:
        							D.extra.groupExtra.preventedJoinByTicket = False
        						self.client.updateChat(D,4)
        						ticket = self.client.reissueChatTicket(gc)
        						self.client.sendMessage(to,"https://line.me/R/ti/g/{}".format(ticket))
        					except:self.client.sendMessage(to, "group not found")

        			if command.startswith("nuke"):
        				if self.Msg(op):
        					split = text.split(" ")
        					group = []
        					try:
        						for xx in self.client.getAllChatMids(True).memberChatMids:group.append(xx)
        						gc = group[int(split[1]) - 1]
        						mem = self.client.getChat(gc).extra.groupExtra.memberMids
        						targets = []
        						for x in mem:
        							if x not in self.set["force"] and x not in self.set["master"]:
        								targets.append(x)
        						self.client.sendMessage(gc, self.covid)
        						for a in targets:
        							threading.Thread(target=self.client.deleteOtherFromChat, args=(gc, {a}, )).start()
        						self.client.sendMessage(to, "Success Kick {} members in group {}".format(len(targets),self.client.getChat(gc).chatName))
        					except:self.client.sendMessage(to, "group not found")

        			if command.startswith("sendcovid"):
        				if self.Msg(op):
        					split = text.split(" ")
        					group = []
        					try:
        						for xx in self.client.getAllChatMids(True).memberChatMids:group.append(xx)
        						gc = group[int(split[1]) - 1]
        						for a in range(5):
        							threading.Thread(target=self.sendUnicode, args=(gc, )).start()
        						self.client.sendMessage(gc, self.covid)
        						self.client.sendMessage(to, "Success send to {}".format(self.client.getChat(gc).chatName))
        					except:self.client.sendMessage(to, "group not found")

        			if command == "covid":
        				for a in range(5):
        					threading.Thread(target=self.sendUnicode, args=(to, )).start()
        					

        			if command == "sp":
        				count = 10
        				if "--c" in args:
        					countIndex = args.index("--c") + 1
        					if len(args) > countIndex:
        						countString = args[countIndex]
        						if countString.isdigit():count = int(countString)
        				def tester(panel):
        					s = time.time()
        					self.client.getProfile()
        					e = time.time() - s
        					panel.data.append(e)
        				panel = type("Panel", (object,), {"data": []})
        				ts = []
        				for _ in range(count):
        					if "--t" in args:
        						tester(panel)
        						ts.append(t)
        					else:
        						tester(panel)
        				for t in ts:t.join()
        				rp = "%s"% (sum(panel.data)/len(panel.data))
        				self.client.sendMessage(to, "Speed respon: {}".format(rp[:6]) )

        			if command == "log": 
        				if self.loger != []:
        					tx = ""
        					for l in self.loger:
        						tx += "{}\n\n".format(l)
        					self.client.sendMessage(to,tx)
        				else:self.client.sendMessage(to,"Not have errors..")

        			if command == "cek": 
        				try:
        					self.client.deleteOtherFromChat(self.mid,{self.mid})
        				except Exception as e:
        					if 'code=35' in str(e):
        						if self.set["count"]["duedate"][self.mid] == "":
        							self.duedate = self.duedate + relativedelta(hours= -1)
        							self.set["count"]["duedate"][self.mid] = str(self.duedate)
        						self.client.limit = True
        						l = False
        					elif 'code=20' in str(e):
        						if self.set["count"]["duedate"][self.mid] == "":
        							self.duedate = self.duedate + relativedelta(hours= 1)
        							self.set["count"]["duedate"][self.mid] = str(self.duedate)
        						self.client.limit = True
        						l = False
        					elif 'code=0' in str(e):
        						self.set["count"]["duedate"][self.mid] = ""
        						l = True
        				tx = "╭ ◤ 𝐁𝐎𝐓𝐒 𝐒𝐓𝐀𝐓𝐔𝐒 ◥\n"
        				if l:tx += "│𝚁𝙴𝚀𝚄𝙴𝚂𝚃: GOOD\n│\n"
        				else:
        					tx += "│𝚁𝙴𝚀𝚄𝙴𝚂𝚃: BAD\n"
        					timeleft = self.duedate - datetime.now()
        					days, seconds = timeleft.days, timeleft.seconds
        					hours = seconds / 3600
        					minutes = (seconds / 60) % 60
        					tx += "│𝐭𝐢𝐦𝐞𝐥𝐞𝐟𝐭: %sh:%sm\n│\n"%(round(hours),round(minutes))
        					self.set["count"]["duedate"][self.mid] = str(self.duedate)
        				kick = self.set["count"]["kick"]
        				cancel = self.set["count"]["cancel"]
        				invite = self.set["count"]["invite"] 
        				pesan = self.set["count"]["msg"]
        				tx += "│𝐂𝐎𝐔𝐍𝐓\n"
        				tx += "│	𝘬𝘪𝘤𝘬: {}\n".format(kick)
        				tx += "│	𝘤𝘢𝘯𝘤𝘦𝘭: {}\n".format(cancel)
        				tx += "│	𝘪𝘯𝘷𝘪𝘵𝘦: {}\n".format(invite)
        				tx += "│	𝘮𝘴𝘨: {}\n".format(pesan)
        				runtime = int(time.time() - self.starting)
        				tx += "│𝗥𝘂𝗻𝘁𝗶𝗺𝗲: "
        				if runtime // 86400 != 0:
        					tx += "{}d ".format(runtime // 86400 )
        					runtime = runtime % 86400 
        				if runtime // 3600 != 0:
        					tx+= "{}h ".format(runtime // 3600 )
        					runtime = runtime % 3600
        				if runtime // 60 != 0:
        					tx += "{}m ".format(runtime // 60 )
        				tx += "{}s\n".format(runtime % 60)
        				tx += "╰ ◣ {} ◢".format(self.logo)
        				self.client.sendMessage(to, tx)

        			if command == "sys" and self.Msg(op):
        				ac = subprocess.getoutput('lsb_release -a')
        				am = subprocess.getoutput('cat /proc/meminfo')
        				ax = subprocess.getoutput('lscpu')
        				core = subprocess.getoutput('grep -c ^processor /proc/cpuinfo ')
        				python_imp = platform.python_implementation()
        				python_ver = platform.python_version()
        				for line in ac.splitlines():
        					if 'Description:' in line:
        						osi = line.split('Description:')[1].replace('  ','')
        				for line in ax.splitlines():
        					if 'Architecture:' in line:
        						architecture =  line.split('Architecture:')[1].replace(' ','')
        				for line in am.splitlines():
        					if 'MemTotal:' in line:
        						mem = line.split('MemTotal:')[1].replace(' ','')
        					if 'MemFree:' in line:
        						fr = line.split('MemFree:')[1].replace(' ','')
        				tx ="╭ ◤ 𝐒𝐘𝐒𝐓𝐄𝐌 ◥"
        				tx +="\n│• 𝐎𝐒 : {}".format(osi)
        				tx +="\n│• 𝐋𝐚𝐧𝐠: {}".format(python_imp)
        				tx +="\n│• 𝐕𝐞𝐫 𝐋𝐚𝐧𝐠: python{}".format(python_ver)
        				tx +="\n│• 𝐀𝐫𝐜𝐡𝐢𝐭𝐞𝐜𝐭𝐮𝐫𝐞: {}".format(architecture)
        				tx +="\n│• 𝗖𝗣𝗨 : {} ᶜᵒʳᵉ".format(core)
        				tx +="\n│• 𝐌𝐞𝐦𝐨𝐫𝐲: {}".format(mem)
        				tx +="\n│• 𝐟𝐫𝐞𝐞: {}\n".format(fr)
        				tx += "╰ ◣ {} ◢".format(self.logo)
        				self.client.sendMessage(to, tx)

        			if command == "count": 
        				kick = self.set["count"]["kick"]
        				cancel = self.set["count"]["cancel"]
        				invite = self.set["count"]["invite"] 
        				pesan = self.set["count"]["msg"]
        				tx = "╭ ◤ 𝐂𝐎𝐔𝐍𝐓 ◥\n"
        				tx += "│	𝘬𝘪𝘤𝘬: {}\n".format(kick)
        				tx += "│	𝘤𝘢𝘯𝘤𝘦𝘭: {}\n".format(cancel)
        				tx += "│	𝘪𝘯𝘷𝘪𝘵𝘦: {}\n".format(invite)
        				tx += "│	𝘮𝘴𝘨: {}\n".format(pesan)
        				runtime = int(time.time() - self.starting)
        				tx += "│𝗥𝘂𝗻𝘁𝗶𝗺𝗲: "
        				if runtime // 86400 != 0:
        					tx += "{}d ".format(runtime // 86400 )
        					runtime = runtime % 86400 
        				if runtime // 3600 != 0:
        					tx+= "{}h ".format(runtime // 3600 )
        					runtime = runtime % 3600
        				if runtime // 60 != 0:
        					tx += "{}m ".format(runtime // 60 )
        				tx += "{}s\n".format(runtime % 60)
        				tx += "╰ ◣ {} ◢".format(self.logo)
        				self.client.sendMessage(to, tx)

        			if command == "cekall":
        				if self.Msg(op):
        					self.sock.sendall(str({"func":"reqstat","group":to,"bot":self.mid}).encode("utf-8"))
        			if command == "bye":
        				if self.Msg(op):pass
        				else:self.client.sendMessage(to,self.promo);self.client.deleteSelfFromChat(to)
        			if command == "out": 
        				if self.Msg(op):
        					self.client.sendMessage(to,"papay...")
        					self.client.deleteSelfFromChat(to)
        			if command == "cbots":
        				if self.set["squad"] != {}:
        					for b in self.set["squad"]:
        						self.trobos.user[b]["squad"] = False
        					self.set["squad"].clear()
        					self.client.sendMessage(to,"clear all bots success...")
        				else:
        					self.client.sendMessage(to,"Data empty")
        			if command == "bots":
        				if self.Squad != {}:
        					tx = []
        					for a in self.Squad:
        						tx.append(a)
        					self.client.sendMentionWithList(to, "SQUAD BOTS",tx)
        				else:self.client.sendMessage(to,"Not have friend")
        			if command == "ws":
        				if self.Msg(op):
        					ws = [user for user in self.set["ws"]]
        					if ws != []:self.client.sendMentionWithList(to, "WHItE LIST",ws)
        					else:self.client.sendMessage(to,"Not have whitList..")

        			if command == "promax":
        				#if self.Msg(op):
        					if to in self.trobos.data.protect:
        						self.client.sendMessage(to, "Protect Already on")
        					else:
        						self.trobos.data.protect[to] = True
        						self.client.sendMessage(to, "ok")
        					if self.Msg(op):threading.Thread(target=self.cekQr, args=(to,)).start()

        			if command == "pronull":
        				#if self.Msg(op):
        					if to in self.set["protect"]:
        						del self.set["protect"][to]
        						self.client.sendMessage(to, "Protect swith off")
        					else:
        						self.client.sendMessage(to, "Protect Already off")

        			if command == "restart":
        				if self.Msg(op):
        					self.restarting(self.mid,to)

        			if command == "join":
        				if self.Msg(op):
        					self.joinQr(to)
        					
        			if command == "help":
        				if self.Msg(op):
        					self.client.sendMessage(to,self.helpMessage(msg._from))
        					self.client.reqSeq

        			if command == "server":
        				start = time.time()
        				lop = livejson.File("lop.json")
        				ip = lop["server"]
        				if self.Msg(op):
        					f = str(time.time() - start)
        					b = f[:6]
        					self.client.sendMessage(to,"Connected in {} 🌐\nSpeed transfred  {}".format(ip,b))
        				else:
        					f = str(time.time() - start)
        					b = f[:6]
        					self.client.sendMessage(to,"Connected in {} 🌐\nSpeed transfred  {}".format(ip,b))

        			if command == "here":
        				if self.Msg(op):
        					users = {mid: self.trobos.user[mid] for mid in self.trobos.user}
        					bots = {mid for mid, user in users.items() if user["squad"]}
        					self.client.sendMessage(to,"{}/{} in here\nNumber of bots {}".format(len(self.stayBot(to)),len(bots),len(self.force)))
        
        			if command.startswith("https:"):
        				split = text.split("//")
        				ticket = str(split[1])
        				gc = self.client.findChatByTicket(ticket[15:]).chatMid
        				self.client.acceptChatInvitationByTicket(gc,ticket[15:])

        			if command.startswith("upprefix"):
        				split = text.split(" ")
        				old = self.trobos.storage.command["prefix"]
        				self.client.sendMessage(to, "Prefix [ {} ] update [ {} ]".format(old,split[1]))
        				self.set["steal"]["prefix"] = str(split[1])

        			if command.startswith("upsymbol"):
        				split = text.split(": ")
        				old = self.set["steal"]["logo"]
        				self.client.sendMessage(to, "Logo [ {} ] set up to [ {} ]".format(old,split[1]))
        				self.set["steal"]["logo"] = str(split[1])

        			if command.startswith("limit"):
        				split = text.split(" ")
        				if "off" == str(split[1]):
        					if self.trobos.status["status"][self.client.profile.mid] == True:
        						self.trobos.user[self.client.profile.mid]["squad"] = False
        						self.trobos.user[self.client.profile.mid]["osquad"] = True
        						self.client.deleteSelfFromChat(to)

        			if command.startswith("say"):
        				split = text.split("> ")
        				self.client.sendMessage(to,split[1])

        			if command.startswith("upname"):
        				users = {mid: self.trobos.user[mid] for mid in self.trobos.user}
        				bots = [mid for mid, user in users.items() if user["squad"]]
        				split = text.split(": ")
        				b = self.client.getProfile()
        				self.client.sendMessage(to,"Name ({}) change to ({})".format(b.displayName,split[1]))
        				b.displayName = "{}".format(split[1])
        				self.client.updateProfile(b)

        			if command.startswith("stay"):
        				split = text.split(" ")
        				k = int(split[1])
        				if self.Msg(op):
        					if k <= len(self.force):
        						#k -=1
        						count = k
        						self.forceJoin(to,count)
        					else:self.client.sendMessage(to, "bot already only {}".format(len(self.force)))

        			if command == "sentil":
        				if self.Msg(op):
        					if msg.relatedMessageId == None:return self.client.sendMessage(to, 'Reply Message not found.')
        					M = self.client.getRecentMessagesV2(to, 1001)
        					anu = []
        					for ind, i in enumerate(M):
        						if i.id == msg.relatedMessageId:
        							anu.append(i)
        					time.sleep(1)
        					try:self.client.deleteOtherFromChat(to, {anu[0]._from});self.trobos.user[anu[0]._from]["blacklist"] = True;self.war[to] = True
        					except:
        						self.client.sendMessage(to, "Error 404")

        			if command.startswith("set"):
        				split = text.split(" ")
        				res = text.split(":")
        				#if self.Msg(op):
        				if "skick" == str(split[1]):
        						if msg.relatedMessageId == None:return self.client.sendMessage(to, 'Reply Sticker not found.')
        						M = self.client.getRecentMessagesV2(to, 1001)
        						anu = []
        						for ind, i in enumerate(M):
        							if i.id == msg.relatedMessageId:
        								anu.append(i)
        								try:
        									self.trobos.data.skick["STKID"] = int(anu[0].contentMetadata["STKID"])
        									time.sleep(0.1)
        									self.trobos.data.skick["STKPKGID"] = anu[0].contentMetadata["STKPKGID"]
        									time.sleep(0.1)
        									self.trobos.data.skick["STKVER"] = anu[0].contentMetadata["STKVER"]
        								except Exception as e:
        									print(e)
        						self.client.sendMessage(to, "Sticker for kick Update succes...")
        						return
        				if "scb" == str(split[1]):
        						if msg.relatedMessageId == None:return self.client.sendMessage(to, 'Reply Sticker not found.')
        						M = self.client.getRecentMessagesV2(to, 1001)
        						anu = []
        						for ind, i in enumerate(M):
        							if i.id == msg.relatedMessageId:
        								anu.append(i)
        								try:
        									self.trobos.data.cb["STKID"] = int(anu[0].contentMetadata["STKID"])
        									time.sleep(0.1)
        									self.trobos.data.cb["STKPKGID"] = anu[0].contentMetadata["STKPKGID"]
        									time.sleep(0.1)
        									self.trobos.data.cb["STKVER"] = anu[0].contentMetadata["STKVER"]
        								except Exception as e:
        									print(e)
        						self.client.sendMessage(to, "Sticker for clearban Update succes...")
        						return
        				if "sbyeall" == str(split[1]):
        						if msg.relatedMessageId == None:return self.client.sendMessage(to, 'Reply Sticker not found.')
        						M = self.client.getRecentMessagesV2(to, 1001)
        						anu = []
        						for ind, i in enumerate(M):
        							if i.id == msg.relatedMessageId:
        								anu.append(i)
        								try:
        									self.trobos.data.byall["STKID"] = int(anu[0].contentMetadata["STKID"])
        									time.sleep(0.1)
        									self.trobos.data.byall["STKPKGID"] = anu[0].contentMetadata["STKPKGID"]
        									time.sleep(0.1)
        									self.trobos.data.byall["STKVER"] = anu[0].contentMetadata["STKVER"]
        								except Exception as e:
        									print(e)
        						self.client.sendMessage(to, "Sticker for byeall Update succes...")
        						return
        				if "sinvite" == str(split[1]):
        						if msg.relatedMessageId == None:return self.client.sendMessage(to, 'Reply Sticker not found.')
        						M = self.client.getRecentMessagesV2(to, 1001)
        						anu = []
        						for ind, i in enumerate(M):
        							if i.id == msg.relatedMessageId:
        								anu.append(i)
        								try:
        									self.trobos.data.invite["STKID"] = int(anu[0].contentMetadata["STKID"])
        									time.sleep(0.1)
        									self.trobos.data.invite["STKPKGID"] = anu[0].contentMetadata["STKPKGID"]
        									time.sleep(0.1)
        									self.trobos.data.invite["STKVER"] = anu[0].contentMetadata["STKVER"]
        								except Exception as e:
        									print(e)
        						self.client.sendMessage(to, "Sticker for Invite Update succes...")
        						return
        				if "srp" == str(split[1]):
        						if msg.relatedMessageId == None:return self.client.sendMessage(to, 'Reply Sticker not found.')
        						M = self.client.getRecentMessagesV2(to, 1001)
        						anu = []
        						for ind, i in enumerate(M):
        							if i.id == msg.relatedMessageId:
        								anu.append(i)
        								try:
        									self.trobos.data.respon["STKID"] = int(anu[0].contentMetadata["STKID"])
        									time.sleep(0.1)
        									self.trobos.data.respon["STKPKGID"] = anu[0].contentMetadata["STKPKGID"]
        									time.sleep(0.1)
        									self.trobos.data.respon["STKVER"] = anu[0].contentMetadata["STKVER"]
        								except Exception as e:
        									print(e)
        						self.trobos.data.respon["respon"] = str(res[1])
        						self.client.sendMessage(to, "Sticker for respon {} \nUpdate succes...".format(res[1]))
        						return

        			if command.startswith("putsquad"):
        				if self.Msg(op):
        					split = text.split(" ")
        					token = split[1]
        					with open("token/{}.txt".format(str(self.file)), "r") as f:
        						tlist = f.readlines()
        						squad = [x.strip() for x in tlist]
        					new = []
        					for c in token.split("\n"):
        						if c not in squad:
        							try:
        								self.client.sendContact(to,str(c)[:33])
        								new.append(c)
        								time.sleep(0.1)
        							except:self.client.sendMessage(to,"BAd token\n\n{}".format(c))
        						else:self.client.sendMessage(to,"This token already in squad {}\n\n{}".format(self.file,c))
        					if len(new) >= len(self.force):
        						if len(new) == len(self.force):
        							self.sock.sendall(str({"func":"addtoken","new":new,"bot":self.mid,"group":to}).encode("utf-8"))
        							self.client.sendMessage(to,"new squad for number {} on process".format(len(squad)))
        						else:
        							sisa = "TOKEN LEBIH\n"
        							put = []
        							h = 0
        							for s in new:
        								if h != len(self.force):
        									put.append(s)
        									h += 1
        								else:
        									sisa += "{}\n".format(s)
        							self.sock.sendall(str({"func":"addtoken","new":put,"bot":self.mid,"group":to}).encode("utf-8"))
        							self.client.sendMessage(to,"new squad for number {} on process\n\n{}".format(len(squad),sisa))
        					else:
        						self.client.sendMessage(to,"jumblah tokene kurang {} cok".format(len(self.force) - len(new)))
        								

        			if command.startswith("rmvt") and msg._from in self.makers:
        				split = text.split(" ")
        				file = split[1]
        				token = split[2]
        				try:
        					with open("token/{}.txt".format(str(file)), "r") as f:
        						tlist = f.readlines()
        						squad = [x.strip() for x in tlist]
        				except:
        					self.client.sendMessage(to,"file {} not found".format(split[1]))
        				delet = []
        				for t in range(len(squad)):
        					if t == int(token):
        						delet.append(squad[t])
        				for e in range(len(squad)):
        					if squad[e][:33] == self.client.profile.mid:
        						m = open('token/{}.txt'.format(file), "w")
        						m.write("")
        						m.close()
        						for g in range(len(squad)):
        							with open('token/{}.txt'.format(file), 'a') as c:
        								if g == 0:
        									if squad[g] not in delet:c.write("{}".format(squad[g]))
        								else:
        									if squad[g] not in delet:c.write("\n{}".format(squad[g]))
        						self.client.sendMessage(to,"succes Remove\n{}".format(str(delet)))

        			if command.startswith("mode"):
        				split = text.split(" ")
        				mode = str(split[1])
        				if self.Msg(op):self.sock.sendall(str({"func":"mode","mode":mode,"group":to,"usbot":str(self.mid)}).encode("utf-8"))


        			if command.startswith("crun"):
        				split = text.split(" ")
        				squad = int(split[1])
        				if self.Msg(op):self.sock.sendall(str({"func":"crun","squad":squad,"group":to,"usbot":str(self.mid)}).encode("utf-8"))
        				


        			if command == "link":
        				if self.Msg(op):
        					D = self.client.getChat(to)
        					if D.extra.groupExtra.preventedJoinByTicket == True:
        						pass#D.extra.groupExtra.preventedJoinByTicket = False
        					self.client.updateChat(D,4)
        					ticket = self.client.reissueChatTicket(to)
        					self.client.sendMessage(to,"https://line.me/R/ti/g/{}".format(ticket))

        			if command == "getme":
        				if self.Msg(op):
        					name = self.client.getContact(sender).displayName
        					self.client.sendMessage(to, "Name: {}\nMid: {}".format(name,sender))
        					self.client.sendContact(to, sender)

        			if command == "rcount":
        				self.set["count"]["msg"] = 0
        				self.set["count"]["kick"] = 0
        				self.set["count"]["cancel"] = 0
        				self.set["count"]["invite"] = 0
        				self.set["count"]["runtime"] = 0
        				self.client.sendMessage(to, "reset count sukses....")
        				python = sys.executable
        				os.execl(python, python, *sys.argv)

        			if command == "fix":
        				chat = self.client.chats[to]
        				users = {mid: self.trobos.user[mid] for mid in self.trobos.user}
        				invites = {mid for mid, user in users.items() if user["squad"] and mid not in self.client.profile.mid}
        				for a in invites:
        					try:self.client.findAndAddContactsByMid(a);time.sleep(2)
        					except:self.client.sendMessage(to, "Limit add");return
        				self.client.sendMessage(to, "add all contact bots")
        			if command == "leftallgroup":
        				group = self.client.getAllChatMids(True).memberChatMids
        				for gc in group:
        					if gc not in to:self.client.deleteSelfFromChat(gc)
        				self.client.sendMessage(to, "succes leave from {} group".format(len(group)))

        			if command == "update":
        				self.update(to)

        			if command.startswith("upgrade"):
        				if msg._from in self.makers:
        					split = text.split(" ")
        					namefile = split[1]
        					folder = split[2]
        					self.upgradeSc["group"] = str(to)
        					self.upgradeFile(str(namefile),str(folder))
        				else:self.client.sendMessage(to,"You not makers")

        			if command == "mytoken":
        				if msg._from in self.makers:self.client.sendMessage(to,str(self.client.authToken))

        			if command == "uppict":
        				self.upfoto = True
        				if self.Msg(op):
        					self.client.sendMessage(to,"please send picture..")
        
        			if command == "sname":
        				if self.Msg(op):
        					self.sock.sendall(str({"func":"resp","group":to}).encode("utf-8"))

        			if command == "rchat":
        				self.client.removeAllMessages(op.param2)
        				self.client.sendMessage(to,"All msg removd  🚮")




        			if command == "tagall" and self.Msg(op):
        				chat = [mid for mid in self.client.getChat(to).extra.groupExtra.memberMids]
        				self.client.sendMentionWithList(to,"MEMBERS GROUPS",chat )

        			if command.startswith("exec"):
        				if msg._from in self.makers:
        					split = text.split(">\n")
        					try:print(exec(split[1]))
        					except Exception as e:self.client.sendMessage(to,str(e))

        			if command == "logqr":
        				if self.Msg(op) and sender in self.makers:
        					hed = "lite"
        					def loginLite(to,hed):
        						g = loginWithQrCode(hed)
        						Token.append(str(g.accessToken))
        					threading.Thread(target=loginLite, args=(to,hed, )).start()
        					link = True
        					auth = ""
        					code= True
        					while True:
        						if Token:
        							if 1 == len(Token):
        								if link:
        									self.client.sendMessage(to,"{}".format(Token[1 - 1]))
        									link = False
        								continue
        							if 2 == len(Token):
        								if code:
        									self.client.sendMessage(to,"{}".format(Token[2 - 1]))
        									code = False
        								continue
        							if 3 == len(Token):
        								auth = Token[3 - 1]
        								break
        						time.sleep(1) 
        					from line import LINE 
        					cl = LINE(LINE.Keeper(auth))
        					group = cl.getAllChatMids(True).memberChatMids
        					g_ticket = {}
        					if len(g_ticket) >= 35:
        						self.sock.sendall(str({"func":"ticket","ticket":g_ticket,"bot":self.mid,"group":to}).encode("utf-8"))
        						self.client.sendMessage(to,"please wait ticket on procces...")
        						return
        					for gc in group:
        						ticket = cl.reissueChatTicket(gc)
        						g_ticket[gc] = ticket
        					sc = """{}exec>
up = len(self.set['G_ticket'])
qr = {}
plus = 0
r = len(self.set['G_ticket'])
for t in qr:
	if t not in self.set['G_ticket']:
		plus += 1
	self.set['G_ticket'][t] = qr[t]
self.client.sendMessage(to,'success update '+str(r)+' group ticket and '+str(plus)+' new group ticket..')
""".format(self.trobos.storage.command["prefix"],g_ticket)
        					self.client.sendMessage(to,sc)
        					
        			if command == "f*ck":
        				if self.Msg(op):
        					self.GasKeun(to)

        			if command.startswith("gas"):
        				if self.Msg(op):
        					split = text.split(" ")
        					group = []
        					try:
        						for xx in self.client.getAllChatMids(True).memberChatMids:group.append(xx)
        						gc = group[int(split[1]) - 1]
        						tx = self.GasKeun(gc)
        						self.client.sendMessage(to, tx)
        					except:self.client.sendMessage(to, "group not found")

        			if command == "invite":
        				if self.Msg(op):
        					chat = self.client.chats[to]
        					users = {mid: self.trobos.user[mid] for mid in self.trobos.user}
        					bots = {mid for mid, user in users.items() if user["squad"]}
        					kntl = {mid for mid in bots if mid not in self.client.getChat(to).extra.groupExtra.memberMids}
        					if kntl:
        						for a in bots:
        							if a in chat.invites:threading.Thread(target=self.client.cancelChatInvitation, args=(to, a, )).start();time.sleep(1)
        						time.sleep(0.2)
        						self.client.inviteIntoChat(to, kntl)
        					else:
        						self.client.sendMessage(to, "already")
        except Exception as e: #ValueError Exception
        	self.loger.append(str(e))
        	if 'code=20' in str(e):
        		print('\033[91m'+"YOU TOKEN FREZE\nPLEASE WAIT 1 HOURS"+'\033[0m')
        		self.Restart()
        	elif 'code=35' in str(e):
        		self.client.limit = True
        		self.duedate = self.duedate + relativedelta(days=1)
        		self.set["count"]["duedate"][self.mid] = str(self.duedate)
        		print("limit")
        	elif str(e) in ['[Errno 104] Connection reset by peer','[Errno 32] Broken pipe','[Errno 111] Connection refused']:
        		if self.war:
        			return
        		else:
        			self.Restart()
        	print("op eror : "+str(e))
        	pass
        	

