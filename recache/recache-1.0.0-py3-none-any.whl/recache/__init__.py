def cache(f, cache = {}):
    def wrapper(*args):
        if args not in cache: cache[args] = f(*args)
        return cache[args]
    return wrapper