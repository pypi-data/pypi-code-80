import asyncio

from ..db import BotifyDatabase
from .config import BotifyConfig
from .storage import BotifyStorage
from .default import DEFAULT_STRINGS
from .media import BotifyMedia
from ..utils import BotifyLogger, Container
from ..engine import BotifyButton
from ..engine import BotifyEngine


from flask import Flask
from flask_migrate import Migrate, init, migrate, upgrade
from sqlalchemy import inspect, or_, and_

from threading import Thread
from aiogram import Bot, Dispatcher, executor

class Botify():

    instance = None

    def __init__(self):

        config = BotifyConfig(self)
        self.config = config
        self.context = config.props
        self.app = Flask(config.name)
        self.logger = BotifyLogger(config.name)
        self.config.logger = BotifyLogger("config", self.logger)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = config.db_uri
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

        self.db = BotifyDatabase(self)
        self.migrate = Migrate(self.app, self.db)

        self.loop = None
        self.bot = Bot(config.token)
        self.dispatcher = Dispatcher(self.bot, storage = BotifyStorage(self))    
        self.medialib = BotifyMedia(self)
        self.engine = BotifyEngine(self)
        self.setup_strings()

        # ENGINE
        self.first_start = self.engine.first_start
        self.start = self.engine.start
        self.message = self.engine.message
        self.button = self.engine.button
        self.admin = self.engine.admin
        self.admin_button = self.engine.admin_button
        self.admin_message = self.engine.admin_message

        self.to_message = self.engine.to_message

        self.build_text = self.engine.build_text
        self.build_cols = self.engine.build_cols
        self.build_pagination = self.engine.build_pagination
        self.render = self.engine.render
        
        self.send = self.engine.send
        self.edit = self.engine.edit
        self.delete = self.engine.delete
        self.notify = self.engine.notify
        self.modal = self.engine.modal

        self.or_ = or_
        self.and_ = and_

        self.check_subscriptions = self.engine.check_subscriptions
        self.is_subscribed = self.engine.is_subscribed

    def __new__(cls):
        if not cls.instance: cls.instance = super(Botify, cls).__new__(cls)
        return cls.instance

    def setup_strings(self):
        
        config = self.config
        self.strings = Container(**DEFAULT_STRINGS)
        strings = config.strings
        if strings:
            for string, value in strings.items():
                self.strings[string] = value

    def __setattr__(self, attribute, value): self.__dict__[attribute] = value
    def __getattr__(self, attribute, default = None): return self.__dict__.get(attribute, default)

    def upgrade_db(self):

        with self.app.app_context():

            try: init()
            except BaseException: pass

            try: migrate()
            except BaseException: pass

            try: upgrade()
            except BaseException: pass

    def run_bot(self): 
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        executor.start_polling(self.dispatcher, loop = self.loop, on_startup = self.medialib.update_media)

    def run(self):
        self.upgrade_db()
        Thread(target = self.run_bot).start()
