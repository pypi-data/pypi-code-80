import asyncio
from datetime import datetime

# provider has flag for request / response 

class KrossProvider:
    def __init__(self, socket, node):
        self.sock = socket
        self.node = node
        self.pending = False
        self.subscribe_count = 0
        self.write_lock = asyncio.Lock()

    async def send_request(self, query):
        async with self.write_lock:
            print('send request done')
            await self.sock.send(query.SerializeToString())

    async def listen(self):
        while True:
            try:
                recv_data = await self.sock.recv()
            except Exception as e:
                print(e)
                break
