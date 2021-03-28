from .async_client import AsyncClient



class AsyncStockProvider(AsyncClient):
    def __init__(self, client, ws, callback):
        super().__init__(client, ws)
        self.start_listening(callback)

