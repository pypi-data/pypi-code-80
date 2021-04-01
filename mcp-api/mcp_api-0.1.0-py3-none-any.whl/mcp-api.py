from requests import get
from base64 import b64decode
from json import dumps, loads

class McpAPI:
    def __init__(self, nickname):
        self.username = nickname
        self.version = '1.0.0'
    
    def is_new_version(self):
        request_version = get('https://raw.githubusercontent.com/julheer/mcp-api/main/version.txt').text.replace('\n', '')
        if request_version.lower() != self.version.lower():
            print(f'[McpAPI] A new version of the library is available. ({request_version})')
            return True
        else:
            return False

    def get_user_uuid(self):
        return get(f'https://api.mojang.com/users/profiles/minecraft/{self.username}').json()['id']
    
    def get_user_skin(self):
        request = get(f'https://sessionserver.mojang.com/session/minecraft/profile/{self.get_user_uuid()}').json()
        return loads(bytes(b64decode(request['properties'][0]['value'])).decode('utf8').replace("'", '"'))['textures']['SKIN']['url']
    
    def get_user_nicknames(self):
        request = get(f'https://api.mojang.com/user/profiles/{self.get_user_uuid()}/names').json()

        nicknames = []
        for nickname in request:
            if 'changedToAt' in request:
                nicknames.append({'nickname': nickname['name'], 'is_default': False, 'changed_at': nickname['changedToAt']})
            else:
                nicknames.append({'nickname': nickname['name'], 'is_default': True, 'changed_at': 0})
        
        return nicknames
    
    def get_blocked_servers(self):
        return get('https://sessionserver.mojang.com/blockedservers').json()
