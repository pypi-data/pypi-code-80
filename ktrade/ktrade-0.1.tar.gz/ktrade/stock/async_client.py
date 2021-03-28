import uuid
import asyncio


class AsyncClient:
    def __init__(self, client, ws):
        self.client = client
        self.ws = ws
        self.listen_task = None

    def _fill_uuid(self, msg):
        msg_id = uuid.uuid4().int
        msg.uuid_h = msg_id >> 64
        msg.uuid_l = msg_id & (1 << 64) -1

    def start_listening(self, callback):
        self.listen_task = asyncio.create_task(self.listening(callback))

    async def listening(self, callback):
        while True:
            try:
                print('start listening')
                recv_data = await self.ws.recv()
                callback(recv_data, socket=self.ws)
            finally:
                pass
