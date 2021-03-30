import re
from sqlalchemy import inspect, text, func
from traceback import format_exc
from datetime import datetime
from ..utils import BotifyLogger, Container

class BotifyQuery():

    def __init__(self, model, botify, db):
        self.db = db
        self.model = model
        self.botify = botify
        self.logger = BotifyLogger(model.__name__.lower(), db.logger)
        self.update_columns()

    def update_columns(self):
        for column in inspect(self.model).columns:
            setattr(self, column.name, column)

    def __setattr__(self, attribute, value): self.__dict__[attribute] = value
    def __getattr__(self, attribute, default = None): return self.__dict__.get(attribute, default)

    # Utils

    def __update_row(self, row, data):
        for key, value in data.items():
            row_value = getattr(row, key)
            if type(value) is str:
                if value.startswith("+") and value[1:].replace(".", "").isdigit(): value = row_value + float(value[1:])
                elif value.startswith("-") and value[1:].replace(".", "").isdigit(): value = row_value - float(value[1:])
                elif value.startswith("!") and type(row_value) is bool: value = not row_value
            setattr(row, key, value)

    def __determine_value(self, value: str):
        value = value.strip()
        if value.startswith("'") and value.endswith("'"): return value[1:-1]
        if value.startswith('"') and value.endswith('"'): return value[1:-1]
        case_insensitive = value.lower()
        
        # Boolean
        if case_insensitive == "false": return False
        if case_insensitive == "true": return True

        # Integer
        if value.isdecimal(): return int(value)

        # Float
        if value.replace(",", ".").replace(".", "").isdigit():
            return float(value.replace(",", "."))

        return value
        
    def __prepare_filters(self, filters):
        _filters = []
        for _filter in filters:
            if type(_filter) is str:
                try:
                    splitted = re.split(r"[> <=!\[]+", _filter)
                    column = splitted[0]
                    value = self.__determine_value(splitted[1])
                    operation = _filter.replace(column, "").replace(splitted[1], "").strip()

                    if "starts" in operation: _filter = eval(f"self.{column}.startswith({value!r})")
                    if "ends" in operation: _filter = eval(f"self.{column}.endswith({value!r})")
                    if "contains" in operation: _filter = eval(f"self.{column}.ilike({value!r})")
                    else: _filter = eval(f"self.{column} {operation} {value!r}")

                except: self.logger.error(format_exc())
            _filters.append(_filter)
        return _filters

    def __prepare_order_by(self, order_by, reverse = False):
        _order_by = []
        for sorter in order_by:
            if type(sorter) is str:
                try:
                    column = getattr(self, sorter.replace("-", "").replace("+", ""))
                    if sorter.startswith("-"): sorter = column.asc() if reverse else column.desc()
                    else: sorter = column.desc() if reverse else column.asc()
                except: self.logger.error(format_exc())
            _order_by.append(sorter)
        return _order_by

    # Inserting

    def add(self, data = None, **kwargs):
        try:
            if data is None: data = {}
            data.update(kwargs)

            # Check if id is already in database
            if "id" in data.keys():
                _id = data.pop("id")
                _object = self.get_by_id(_id)
                if _object: return self.update_by_id(
                    _id, data = Container(**data)
                )

            _object = self.model(**data)
            self.db.session.add(_object)
            self.db.session.commit()
            return _object.serialize()
        except: self.logger.error(format_exc())

    # Selecting

    def get_all(self, *filters, page = 1, limit = 100000, filter_by = None, order_by = None, count = False, serialize = True):
        
        if filter_by is None: filter_by = {}
        if order_by is None: order_by = []
        filters = self.__prepare_filters(filters)
        order_by = self.__prepare_order_by(order_by)

        try:
            query = self.model.query.filter(*filters).filter_by(**filter_by).order_by(*order_by)
            data = query.limit(limit).offset((page - 1) * limit).all()
            if data:
                if serialize: data = self.model.serialize_all(data)
                if count: return data, query.count()
                return data
            else: return ([], 0) if count else []
        except: self.logger.error(format_exc())

    def get(self, *filters, filter_by = None, serialize = True):
        if filter_by is None: filter_by = {}
        filters = self.__prepare_filters(filters)
        try: 
            row = self.model.query.filter(*filters).filter_by(**filter_by).first()
            return row.serialize() if serialize and row else row
        except: self.logger.error(format_exc())

    def get_by_id(self, _id, serialize = True):
        try: 
            row = self.model.query.filter(self.model.id == _id).first()
            return row.serialize() if serialize and row else row
        except: self.logger.error(format_exc())

    def get_last_created(self, serialize = True):
        try: 
            row = self.model.query.order_by(self.model.created.desc()).limit(1).first()
            return row.serialize() if serialize and row else row
        except: self.logger.error(format_exc())

    def get_last_updated(self, serialize = True):
        try: 
            row = self.model.query.order_by(self.model.updated.desc()).limit(1).first()
            return row.serialize() if serialize and row else row
        except: self.logger.error(format_exc())

    def get_rating(self, fields, *filters, filter_by = None, limit = 100, serialize = True):
        if filter_by is None: filter_by = {}
        if not type(fields) in (list, tuple): fields = [fields]
        filters = self.__prepare_filters(filters)
        order_by = self.__prepare_order_by(fields, reverse = True)
        try: 
            data = self.model.query.filter(*filters).filter_by(**filter_by).order_by(*order_by).limit(limit).all()
            if serialize: data = self.model.serialize_all(data)
            return data
        except: self.logger.error(format_exc())

    def get_rating_place(self, _id, fields, *filters, filter_by = None, limit = 100000):
        if filter_by is None: filter_by = {}
        try:
            data = self.get_rating(fields, *filters, filter_by = filter_by, limit = limit)
            for place, row in enumerate(data):
                if row.id == _id: return place + 1
        except: self.logger.error(format_exc())

    # Updating

    def update(self, *filters, filter_by = None, count = False, serialize = True, data = None, **kwargs):
        
        if data is None: data = Container()
        if filter_by is None: filter_by = {}
        if type(data) is Container: data = data.raw()
        data["updated"] = datetime.now().timestamp()
        data.update(kwargs)
        _count = 0
        try:
            result = self.get_all(*filters, filter_by = filter_by, count = count, serialize = False)
            if count:
                rows = result[0]
                _count = result[1]
            else: rows = result
            for row in rows: self.__update_row(row, data)
            self.db.session.commit()
            if serialize: rows = self.model.serialize_all(rows)
            return rows
        except: self.logger.error(format_exc())

    def update_by_id(self, _id, data = None, serialize = True, **kwargs):
        if data is None: data = Container()
        if type(data) is Container: data = data.raw()
        data["updated"] = datetime.now().timestamp()
        data.update(kwargs)
        try:
            row = self.get_by_id(_id, serialize = False)
            self.__update_row(row, data)
            self.db.session.commit()
            return row.serialize() if serialize and row else row
        except: self.logger.error(format_exc())     

    def update_last_created(self, data = None, serialize = True, **kwargs):
        if data is None: data = Container()
        if type(data) is Container: data = data.raw()
        data["updated"] = datetime.now().timestamp()
        data.update(kwargs)
        try:
            row = self.get_last_created(serialize = False)
            self.__update_row(row, data)
            self.db.session.commit()
            return row.serialize() if serialize and row else row
        except: self.logger.error(format_exc())     

    def update_last_updated(self, data = None, serialize = True, **kwargs):
        if data is None: data = Container()
        if type(data) is Container: data = data.raw()
        data["updated"] = datetime.now().timestamp()
        data.update(kwargs)
        try:
            row = self.get_last_updated(serialize = False)
            self.__update_row(row, data)
            self.db.session.commit()
            return row.serialize() if serialize and row else row
        except: self.logger.error(format_exc())     

    # Deleting

    def delete(self, *filters, filter_by = None, count = False, serialize = True):
        if filter_by is None: filter_by = {}
        filters = self.__prepare_filters(filters)
        try:
            query = self.model.query.filter(*filters).filter_by(**filter_by)
            _count = query.count()
            rows = query.all()
            query.delete(synchronize_session = "fetch")
            self.db.session.commit()
            if serialize: rows = self.model.serialize_all(rows)
            return (rows, _count) if count else rows
        except: self.logger.error(format_exc())

    def delete_by_id(self, _id, serialize = True):
        try:
            query = self.model.query.filter(self.model.id == _id)
            row = query.first()
            query.delete(synchronize_session = "fetch")
            self.db.session.commit()
            return row.serialize() if serialize and row else row
        except: self.logger.error(format_exc())     

    def delete_last_created(self, serialize = True):
        try:
            row = self.get_last_created(False)
            self.db.session.delete(row)
            self.db.session.commit()
            return row.serialize() if serialize and row else row
        except: self.logger.error(format_exc())     

    def delete_last_updated(self, serialize = True):
        try:
            row = self.get_last_updated(False)
            self.db.session.delete(row)
            self.db.session.commit()
            return row.serialize() if serialize and row else row
        except: self.logger.error(format_exc())     


