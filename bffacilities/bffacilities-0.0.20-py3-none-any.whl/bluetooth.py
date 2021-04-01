import sys
from bleak import BleakScanner, BleakClient
import asyncio
from time import sleep
import threading, queue
import socket
from datetime import datetime
import json
if sys.platform == "win32":
    from Windows.Devices.Bluetooth.Advertisement import BluetoothLEAdvertisementFilter, BluetoothLEAdvertisement 

class BluetoothMgr() :
    IO_DATA_CHAR_UUID_W  = "0000ffe1-0000-1000-8000-00805f9b34fb"

    def __init__(self, msgQueue):
        self._sockSender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sockSender.bind(("", 12001))
        self._btClient = None
        self._btConnected = False
        self._msgQueue = msgQueue
        self._running = True

        self._peer = None

        self.loop = asyncio.get_event_loop()
        self._devices = { } # key address

    async def listDevice(self, timeout):
        devices = await BleakScanner.discover(timeout=timeout)
        for d in devices:
            if d.address not in self._devices:
                self._devices[d.address] = d
        self.syncDeviceToOther()

    def _detection_callback(self, device, advertisement_data):
        if len(advertisement_data.local_name) is 0:
            return
        if device.address not in self._devices:
            print(f"First [{datetime.now()}] RSSI:", device.rssi, advertisement_data.local_name
                    # ,device.address
                    )
        device.name = advertisement_data.local_name
        self._devices[device.address] = device
        self.syncDeviceToOther()

    def syncDeviceToOther(self):
        if self._peer is None:
            return
        data = []
        for device in self._devices.values():
            name = device.name if hasattr(device, "name") else None
                
            data.append({
                "address": device.address,
                "name": name,
                "rssi": device.rssi
            })
        data = json.dumps(data)
        self._sockSender.sendto(data.encode(), self._peer)

    async def findDevice(self, name = None, seconds = 5.0):

        bleFilter = BluetoothLEAdvertisementFilter()
        if name:
            ad = BluetoothLEAdvertisement()
            ad.put_LocalName(name)
            bleFilter.put_Advertisement(ad)

        scanner = BleakScanner(AdvertisementFilter=bleFilter)
        scanner.register_detection_callback(self._detection_callback)
        # await scanner.set_scanning_filter()
        await scanner.start()
        if seconds < 0:
            seconds = 100
        await asyncio.sleep(seconds)
        await scanner.stop()
        # devices = await scanner.get_discovered_devices()
        # for d in devices:
        #     print(d)
        print("[BT] Find Device Done")


    def _onRecvBtMsg(self, sender, data):
        # print("Recv Bt", sender, data)
        if len(data) > 3 and self._peer:
            self._sockSender.sendto(data, self._peer)
            # print("Recv BT", data)
    async def connectToBLE(self, address):
        self._btClient = BleakClient(address)
        print("[BT] Try Connecting Bluetooth", address)
        # service = await self._btClient.get_services()
        # model_number = await self._btClient.read_gatt_char(BluetoothMgr.IO_DATA_CHAR_UUID_W )
        # print(f"Model Number {model_number}: {''.join(map(chr, model_number))}")
        try:
            self._btConnected = await self._btClient.connect()
            print(f"Client {self._btClient} connected: {self._btConnected}")
            if self._btConnected:
                await self._btClient.start_notify(BluetoothMgr.IO_DATA_CHAR_UUID_W, self._onRecvBtMsg)
            idx = 0
            while self._btConnected:
                if not self._msgQueue.empty():
                    sData = self._msgQueue.get()
                    await self._btClient.write_gatt_char(BluetoothMgr.IO_DATA_CHAR_UUID_W, sData)
                    print("SendData Bt", sData)
                await asyncio.sleep(0.001)
                # if idx >= 20000:
                #     print("RecvBytes From Bt", idx)
                #     idx -= 20000
                # print(f"Model Number: {data}")
                # sleep(0.001)
                # print("Model Number: {0}".format("".join(map(chr, data))))
        except Exception as e:
            self._btConnected = False
            print(f"Exception: {e}")
        finally:
            await self._btClient.disconnect()

        # self._running = False
        print("[BMGR] connect done")     

    async def stop(self):
        print("Stop bluetooth")
        if self._btConnected:
            self._btClient.stop_notify()
            self._btClient.disconnect()
    def processCmd(self, cmd):
        """
        {
            "action": "listDevice",
            "timeout": "60", // seconds
        }

        {
            "action": "findDevice",
            "name": "CMPS", // or no name for find all device
            "timeout": 30, // default 30
        }

        {
            "action": "disconnect" // disconnect if a device has connected
        }

        {
            "action": "quit" // quit program
        }
        """
        action = cmd["action"]
        if action == "listDevice":
            self.loop.run_until_complete(self.listDevice(timeout= cmd.get("timeout", 10)))
        elif action == "findDevice":
            self.loop.run_until_complete(self.findDevice(name=cmd.get("name"), seconds= cmd.get("timeout", 20)))
        elif action == "disconnect":
            self.loop.run_until_complete(self.stop())
        elif action == "quit":
            self._running = False
        else:
            print("Unsupported cmd", action)

    def recvUdp(self):
        self._sockSender.settimeout(0)
        self._sockSender.setblocking(False)
        print("[BT] Start Listening UDP")
        # self._sockSender.sendto(b'test', ("127.0.0.1", 12000))
        while self._running:
            try:
                data = self._sockSender.recvfrom(1024)
                self._peer = data[1]
                cmd = None
                try:
                    cmd = json.loads(data[0])
                except:
                    pass
                if cmd and self.processCmd:
                    self.processCmd(cmd)
                else:
                    self._msgQueue.put(data[0])
                    print("RECV PC", data)
            except KeyboardInterrupt:
                self._running = False
            except Exception as e:
                sleep(0.01)
            sleep(0.001)
                # print(e)

    def start(self):
        try:
            thread = threading.Thread(target = self.recvUdp)
            thread.daemon = True
            thread.start()
            while self._running: sleep(2)
        except (KeyboardInterrupt, SystemExit):
            self._running = False
            print("==========Quit===========")
if __name__ == "__main__":
    btMgr = BluetoothMgr(queue.Queue())
    btMgr.start()