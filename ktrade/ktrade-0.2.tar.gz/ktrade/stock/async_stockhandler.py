from .async_client import AsyncClient


class AsyncStockHandler(AsyncClient):
    def __init__(self, client, ws):
        super().__init__(client, ws)

    async def get_day_data(self, query):
        self._fill_uuid(query)

        await self.ws.send(query.SerializeToString())
        print('waiting recv')
        data = await self.ws.recv()
        return data
