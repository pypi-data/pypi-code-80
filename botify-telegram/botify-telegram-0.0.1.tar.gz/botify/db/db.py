from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from .model import BotifyModel, create_column
from .query import BotifyQuery
from ..utils import BotifyLogger

class BotifyDatabase(SQLAlchemy):

    def __init__(self, botify):
        super().__init__(botify.app, model_class = BotifyModel)
        self.botify = botify
        self.logger = BotifyLogger("database", botify.logger)
        self.models = []
        self.create_defaults()
        self.extend()

    def create_defaults(self):
        self.create(
            "chats",
            ("chat_id", int, "unique")
        )
        
        self.create(
            "media",

            ("tag", str),
            ("type", str),
            ("file_id", str),
            ("path", str)
        )

        self.create(
            "users",   

            ("user_id", int, "unique"),
            ("inviter_id", int, 0),
            ("invited", int, 0),
            ("chat_id", int),
            ("state", str, "none"),
            ("data", str, "{}"),
            ("bucket", str, "{}"),

            ("admin", bool, False),
            ("permissions", int, 1),
            ("firstname", str, ""),
            ("lastname", str, ""),
            ("username", str, "")
        )


    def create(self, name, *columns):
        cols = {}
        botify = self.botify
        extends = self.Model

        for column in columns:
            if not type(column) is Column:
                column = create_column(*column, props = botify.config.props)
            cols[column.name] = column
        
        model = type(name, (extends,), cols)
        query = BotifyQuery(model, botify, self)
        setattr(botify, name.lower(), query)
        self.models.append(model)

        return model

    def extend(self):
        logger = self.logger
        config = self.botify.config
        extensions = config.get("extend-models", {})
        for modelname, columns in extensions.items():
            logger.info(f"Loading extension for model {modelname}")
            extended = False
            _columns = []
            
            for column, data in columns.items():
                logger.info(f"{modelname}: Appending column {column}")
                if not type(data) is list: data = [data]
                _columns.append([column, *data])
            
            for model in self.models:
                if model.__name__.lower() == modelname.lower():
                    model.extend(*_columns, props = config.props)
                    query = getattr(self.botify, modelname.lower())
                    query.update_columns()
                    extended = True
            
            if not extended: 
                logger.info(f"{modelname}: Assigning query object to Botify instance attribute.")
                self.create(modelname.capitalize(), *_columns)
                

    