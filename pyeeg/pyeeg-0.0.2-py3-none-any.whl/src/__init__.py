from websocket import create_connection
import ssl
import json
import sys


class EmotivClient:
    def __init__(self, client_id: str, client_secret: str, profile: str,subscribe: int , url="wss://localhost:6868"):
        self.clientId = client_id
        self.clientSecret = client_secret
        self.profile = profile
        self.url = url
        self.ws = create_connection(self.url, sslopt={"cert_reqs": ssl.CERT_NONE})
        self.isPause = False
        if subscribe == 0:
            self.subscribe = "com"
        elif subscribe == 1:
            self.subscribe = "fac"

    def pause(self):
        if self.isPause:
            self.isPause = False
        else:
            self.isPause = True

    def stop(self):
        sys.exit(0)

    def listen(self, listener: callable, log=print):
        log("Start Connecting!")
        self.ws.send(json.dumps({
            "id": 1,
            "jsonrpc": "2.0",
            "method": "requestAccess",
            "params": {
                "clientId": self.clientId,
                "clientSecret": self.clientSecret
            }
        }))
        self.ws.recv()
        self.ws.send(json.dumps({
            "id": 1,
            "jsonrpc": "2.0",
            "method": "authorize",
            "params": {
                "clientId": self.clientId,
                "clientSecret": self.clientSecret
            }
        }))
        data = self.ws.recv()
        cortex_token = json.loads(data)["result"]["cortexToken"]
        self.ws.send(json.dumps({
            "id": 1,
            "jsonrpc": "2.0",
            "method": "queryHeadsets"
        }))
        data = self.ws.recv()
        device_id = json.loads(data)["result"][0]["id"]
        self.ws.send(json.dumps({
            "id": 1,
            "jsonrpc": "2.0",
            "method": "controlDevice",
            "params": {
                "command": "connect",
                "headset": str(device_id)
            }
        }))
        self.ws.send(json.dumps({
            "id": 1,
            "jsonrpc": "2.0",
            "method": "createSession",
            "params": {
                "cortexToken": cortex_token,
                "headset": str(device_id),
                "status": "open"
            }
        }))
        self.ws.recv()
        self.ws.send(json.dumps({
            "id": 1,
            "jsonrpc": "2.0",
            "method": "querySessions",
            "params": {
                "cortexToken": cortex_token
            }
        }))
        data = self.ws.recv()
        session_id = json.loads(data)["result"]["id"]
        self.ws.send(json.dumps({
            "id": 1,
            "jsonrpc": "2.0",
            "method": "setupProfile",
            "params": {
                "cortexToken": str(cortex_token),
                "headset": str(device_id),
                "profile": self.profile,
                "status": "load"
            }
        }))
        self.ws.recv()
        self.ws.send(json.dumps({
            "id": 1,
            "jsonrpc": "2.0",
            "method": "subscribe",
            "params": {
                "cortexToken": cortex_token,
                "session": str(session_id),
                "streams": [f"{str(self.subscribe)}"]
            }
        }))
        self.ws.recv()
        log("Successfully connected!")
        while not self.isPause:
            try:
                data = self.ws.recv()
                com = json.loads(data).get(f"{self.subscribe}")
                if self.subscribe == "com":
                    self.cmd = com[0]
                    self.intense = com[1]
                else:
                    self.cmd = com[3]
                    self.intense = com[4]
                listener(self.cmd, self.intense)
            except:
                pass
