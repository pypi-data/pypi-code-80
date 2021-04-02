import aiohttp
import asyncio

class AviOnBridge:

    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self._token = None

    async def get_token(self) -> str:
        if self._token is not None:
            return self._token
        
        body = {'email': self._username, 'password': self._password}
        async with aiohttp.ClientSession() as session:
            async with session.post('https://api.avi-on.com/sessions', json=body) as resp:
                if resp.status != 201:
                    print(await resp.text())
                    raise Exception('Error retrieving authorization token.')
                
                json = await resp.json()

                self._token = json['credentials']['auth_token']

                return self._token


    def get_devices(self):
        return []

    
