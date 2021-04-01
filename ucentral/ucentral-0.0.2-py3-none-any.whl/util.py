class Config(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            self[key] = value = Config()
            return value

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def merge(src, dest):
    for key, value in src.items():
        if isinstance(value, dict):
            node = dest.setdefault(key, {})
            merge(value, node)
        else:
            dest[key] = value

    return dest
