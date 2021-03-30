from ..utils import Container
from sqlalchemy import Column, inspect
from sqlalchemy import ARRAY, BLOB, Boolean
from sqlalchemy import Integer, DateTime, Float
from sqlalchemy import String, JSON
from datetime import datetime, time

def now(): return datetime.now().timestamp()

def convert_type(type_, list_):
    if type(type_) is str: type_ = type_.lower()
    if type_ in (list, tuple, "list", "tuple", "array"): return ARRAY(convert_type(list_[2], list_))
    if type_ in (object, "object", "blob"): return BLOB
    if type_ in (bool, "bool", "boolean"): return Boolean
    if type_ in (datetime, "datetime"): return DateTime
    if type_ in (int, "int", "integer"): return Integer
    if type_ in (float, "float", "double"): return Float
    if type_ in (str, "str", "string", "text"): return String
    if type_ in (dict, "dict", "json"): return JSON 

def create_column(*args, props = Container()):
    args = list(args)
    name = args[0]
    type_ = convert_type(args[1], args)

    unique = False
    if "unique" in args: 
        args.remove("unique")
        unique = True

    notnull = False
    if "notnull" in args: 
        args.remove("notnull")
        notnull = True

    primary_key = False
    if "primary_key" in args:
        args.remove("primary_key")
        primary_key = True
        
    default = args[2] if len(args) > 2 else None

    # Evaluate props
    if type(default) is str:
        if default.startswith("props."):
            attribute = default.split(".", maxsplit = 1)[1]
            default = getattr(props, attribute)

    del props

    return Column(
        name, type_, 
        unique = unique, 
        primary_key = primary_key, 
        default = default, 
        nullable = not notnull
    )

class BotifyModel():

    post_permissions_level = 1
    get_permissions_level = 1

    id = Column(Integer, primary_key = True)
    created = Column(Float, default = now)
    updated = Column(Float, default = now)

    @classmethod
    def extend(cls, *columns, props = Container()):
        for column in columns:
            if type(column) is Column: setattr(cls, column.name, column)
            elif type(column) in (tuple, list): setattr(cls, column[0], create_column(*column, props = props))

    @staticmethod
    def serialize_all(objects):
        return [
            _object.serialize() for _object in objects \
            if isinstance(_object, BotifyModel)
        ]

    def __serialize_value(self, value):
        if isinstance(value, datetime): return int(value.timestamp())
        return value

    def serialize(self):
        return Container(**{
            c: self.__serialize_value(getattr(self, c)) \
            for c in inspect(self).attrs.keys() \
        })