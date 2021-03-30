from aiogram.dispatcher.storage import BaseStorage
from ..utils import BotifyLogger
from traceback import format_exc
import json


class BotifyStorage(BaseStorage):
    def __init__(self, botify): 
        self.botify = botify
        self.logger = BotifyLogger("storage", botify.logger)

    async def wait_closed(self): pass
    async def close(self): pass

    def resolve_address(self, chat, user):
        botify = self.botify
        chat, user = self.check_address(chat = chat, user = user)

        chat_ = botify.chats.get(botify.chats.chat_id == chat)
        user_ = botify.users.get(botify.users.user_id == user)
        if not chat_: chat_ = botify.chats.add(chat_id = chat)
        if not user_: user_ = botify.users.add(user_id = user, chat_id = chat)
        return chat_, user_

    async def get_state(self, *, chat = None, user = None, default = None): 
        try: return self.resolve_address(chat, user)[1].state
        except: self.logger.error(f"GET_STATE: {format_exc()}")

    async def get_data(self, *, chat = None, user = None, default = None): 
        try: return json.loads(self.resolve_address(chat, user)[1].data)
        except: self.logger.error(f"GET_DATA: {format_exc()}")
    
    async def get_bucket(self, *, chat = None, user = None, default = None): 
        try: return json.loads(self.resolve_address(chat, user)[1].bucket)
        except: self.logger.error(f"GET_BUCKET: {format_exc()}")

    async def set_data(self, *, chat = None, user = None, data = {}):
        try:
            botify = self.botify
            user = self.resolve_address(chat, user)[1]
            botify.users.update(botify.users.user_id == user.user_id, data = {"data": json.dumps(data, ensure_ascii = False)})
        except: self.logger.error(f"SET_DATA: {format_exc()}")

    async def set_bucket(self, *, chat = None, user = None, bucket = {}):
        try:
            botify = self.botify
            user = self.resolve_address(chat, user)[1]
            botify.users.update(botify.users.user_id == user.user_id, bucket = json.dumps(bucket, ensure_ascii = False))
        except: self.logger.error(f"SET_BUCKET: {format_exc()}")

    async def set_state(self, *, chat = None, user = None, state = ''):
        try:
            botify = self.botify
            state = state.replace("['", "").replace("']", "")        
            user = self.resolve_address(chat, user)[1]
            botify.users.update(botify.users.user_id == user.user_id, state = state)
        except: self.logger.error(f"SET_STATE: {format_exc()}")

    async def reset_state(self, *, chat = None, user = None, with_data = True):
        try:
            botify = self.botify
            user = self.resolve_address(chat, user)[1]
            data = {"state": ""}
            if with_data: data["data"] = "{}"
            botify.users.update(botify.users.user_id == user.user_id, data = data)
        except: self.logger.error(f"RESET_STATE: {format_exc()}")

    async def update_data(self, *, chat = None, user = None, data = {}):
        try:
            botify = self.botify
            user = self.resolve_address(chat, user)[1]
            user_data = json.loads(user["data"])
            user_data.update(data)
            botify.users.update(botify.users.user_id == user.user_id, data = {"data": user_data})
        except: self.logger.error(f"UPDATE_DATA: {format_exc()}")

    async def update_bucket(self, *, chat = None, user = None, bucket = {}):
        try:
            botify = self.botify
            user = self.resolve_address(chat, user)[1]
            user_bucket = json.loads(user["bucket"])
            user_bucket.update(bucket)
            botify.users.update(botify.users.user_id == user.user_id, bucket = user_bucket)
        except: self.logger.error(f"UPDATE_BUCKET: {format_exc()}")