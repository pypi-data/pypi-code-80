import asyncio
import aioredis
from aioredis.commands import Redis

class AsyncRedisConnectHandler:
    def __init__(
        self,
        host: str="redis://localhost",
        port: int=6379,
        db: int=0,
        password: str=None
    ) -> None:
        self.__host: str = host
        self.__port: int = port
        self.__db: int = db
        self.__password: str = password
        self.connect: Redis = None

    def create_pool(self) -> None:
        loop = asyncio.get_event_loop()
        loop.create_task(self.__create_pool())

    def connect_uri(self) -> None:
        loop = asyncio.get_event_loop()
        loop.create_task(self.__connect_uri())

    def connect_tcp(self) -> None:
        loop = asyncio.get_event_loop()
        loop.create_task(self.__connect_tcp())

    def connect_unixsocket(self) -> None:
        loop = asyncio.get_event_loop()
        loop.create_task(self.__connect_unixsocket())
    
    async def __create_pool(self) -> None:
        self.connect = await aioredis.create_redis_pool(
            f"{self.__host}/{self.__db}", 
            password=self.__password
        )

    async def __connect_uri(self) -> None:
        self.connect = await aioredis.create_connection(
            self.__host,
            pasword=self.__password)

    async def __connect_tcp(self) -> None:
        self.conn = await aioredis.create_connection(
            (self.__host, self.__port),
            password=self.__password)

    async def __connect_unixsocket(self) -> None:
        self.conn = await aioredis.create_connection(
            self.__host,
            password=self.__password)

    async def disconnect(self) -> None:
        self.pool.close()
        await self.pool.wait_closed()

    def change_host(self, host: str) -> None:
        self.__host = host

    def change_port(self, port: int) -> None:
        self.__port = port

    def change_db(self, db: int) -> None:
        self.__db = db

    def change_host(self, password: str) -> None:
        self.__password = password