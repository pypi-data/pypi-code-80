import time
import os
import sys
import json
import Tkinter as tk
from threading import Thread
from ws4py.client.threadedclient import WebSocketClient


text_map = {}

class Client(WebSocketClient):
    def get_target_instId(self, instId):
        return '{"args": [{"instId": "' + instId + '", "channel": "candle15m"}], "op": "subscribe"}'

    def opened(self):
        self.data = {}
        self.target_instIds = ["ETH-USDT", "CFX-USDT"]
        for instId in self.target_instIds:
            self.send(self.get_target_instId(instId))

    def closed(self, code, reason=None):
        exit(0)

    def received_message(self, resp):
        try:
            resp = json.loads(unicode(resp))
            data, sign = float(resp['data'][0][4]), str(resp['arg']['instId'])
            text_map[sign].set('{}: {}'.format(sign, data))
        except Exception as e:
            print e.message
            pass


def create_window():
    main = tk.Tk()
    main.title(u"OKEX")
    main.geometry("200x40")
    main.resizable(width=False, height=False)
    main.attributes("-topmost", True)
    return main


def start():
    main = create_window()
    url = 'wss://wspri.coinall.ltd:8443/ws/v5/public'
    ws = Client(url)
    ws.connect()
    t = Thread(target=lambda : ws.run_forever())
    t.setDaemon(True)
    t.start()
    for d in ws.target_instIds:
        t = tk.StringVar()
        x = tk.Label(master=main, textvariable=t)
        text_map[d] = t
        x.pack()

    main.mainloop()