import asyncio

from .protocol import stock_pb2
from . import providerdict


class KrossClient:
    def __init__(self, socket, node):
        self.sock = socket
        self.node = node
        self.write_lock = asyncio.Lock()

    async def send_object(self, data):
        async with self.write_lock:
            await self.sock.send(data.SerializeToString())

    async def send_response(self, query, result_code):
        result = stock_pb2.StockResult()
        result.uuid_h = query.uuid_h
        result.uuid_l = query.uuid_l
        result.code = result_code
        await self.send_object(result)

    async def listen(self):
        while True:
            try:
                recv_data = await self.sock.recv()
                print('recv msg', len(recv_data))
                query = stock_pb2.StockQuery()
                query.ParseFromString(recv_data)
                provider = await providerdict.find_provider(self.node.vendor,
                              self.node.channel_type,
                              self.node.service)

                print(provider)
                if provider is None:
                    await self.send_response(query, stock_pb2.NO_PROVIDER)
                else:
                    await provider.send_request(query)

            except Exception as e:
                print(e)
                break
        print('quit listening...')
