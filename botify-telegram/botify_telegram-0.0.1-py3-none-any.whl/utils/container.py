import json
import yaml
from os import path

class Container():

    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)

    def __convert(self, value):

            if type(value) is dict: 
                __value = {}
                for key, _value in value.items(): __value[key] = self.__convert(_value)
                return Container(**__value)

            if type(value) is list:
                __value = []
                for _value in value: __value.append(self.__convert(_value))
                return __value
            
            return value

    def __repr__(self): return self.__dict__.__repr__()
    def __bool__(self): return bool(self.__dict__)
    def __eq__(self, other): return self.__dict__ == other.__dict__ 

    def to_file(self, _path, mode = "json"):
        with open(_path, "w+", encoding = "utf-8") as _file:
            if mode == "json": json.dump(self.raw(), _file, indent = 4, ensure_ascii = False)
            elif mode == "yaml": yaml.dump(self.raw(), _file, indent = 4, encoding = "utf-8")

    def raw(self):
        result = {}
        for key, value in self.__dict__.items():
            if type(value) is Container: value = value.raw()
            result[key] = value
        return result

    def map(self, function): return {key : function(value) \
                                    for key, value in self.__dict__.items()}


    def filter(self, function): return {key: value for key, value \
                                        in self.__dict__.items() if function(value)}

    def pop(self, key, default = None):

        if key in self.__dict__:
            value = self.__dict__[key]
            self.__dict__.pop(key)
            return value

        return default if default else Container()

    def clear(self): self.__dict__.clear()
    def copy(self): return Container(**self.__dict__.copy())
    
    def __setattr__(self, key, value): self.__dict__[key] = self.__convert(value)
    def __delitem__(self, key): self.__delattr__(key)
    def __delattr__(self, key): 
        if key in self.__dict__.keys(): 
            del self.__dict__[key]
    def __getattr__(self, key, default = None): return self.__dict__.get(key, default if default else Container())
    def __getitem__(self, index): return self.__dict__.get(index, Container())
    def __setitem__(self, index, value): self.__dict__[index] = self.__convert(value)
    def get(self, key, default = None): return self.__dict__.get(key, default)
    def items(self): return self.__dict__.items()
    def keys(self): return list(self.__dict__.keys())
    def values(self): return list(self.__dict__.values())
    
    def update(self, obj): 
        if type(obj) is Container:
            for key, value in obj.items():
                self.__dict__[key] = self.__convert(value)

        elif type(obj) is dict:
            for key, value in obj.items():
                self.__dict__[key] = self.__convert(value) 
    
    def deep_update(self, source):
       
        if not type(source) is Container: source = Container(**source)

        for key, value in source.items():
            if key in self.__dict__.keys():
                _value = self.__dict__[key]
                if type(value) in (Container, dict):
                    if type(_value) is Container:
                        _value.deep_update(value)
                        value = _value.copy()

            setattr(self, key, value)
    

        