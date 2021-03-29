from .async_client import AsyncClient


class AsyncStockSubscriber(AsyncClient):
    def __init__(self, client, ws, callback):
        super().__init__(client, ws)
        self.start_listening(callback)


    async def subscribe_stock(self, symbol):
        pass
