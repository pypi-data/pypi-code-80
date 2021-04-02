import json
import pkgutil

BAND_DATA_FILE = 'data/map.json'
BAND_MAP = None

Coords = tuple[str, int, int]


def get_map():
    global BAND_MAP
    if BAND_MAP is None:
        data = pkgutil.get_data('leapdna', BAND_DATA_FILE)
        map_with_lists = json.loads(data)
        BAND_MAP = {key: tuple(value) for key, value in map_with_lists.items()}

    return BAND_MAP


def decrease_band_precission(name):
    """Returns the parent band of the given band, e.g. calling this function
    repeatedly starting with 3p12.31a would yield the following results:
    3p12.31a, 3p12.31, 3p12.3, 3p12, 3p1, 3p, 3"""
    if len(name) > 2 and name[-2] == '.':
        return name[:-2]

    return name[:-1]


def band2coords(band):
    """Given the name of a band it returns a tuple (chr, start, stop) with the
    coordinates of that band. If the coordinates are not known it returns None."""
    if band == '': return None

    try:
        return get_map()[band]
    except KeyError:
        return band2coords(decrease_band_precission(band))
