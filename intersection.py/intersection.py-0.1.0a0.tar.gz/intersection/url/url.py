# A class storing all the urls that are used
import pip._vendor.requests as requests
import json

class URLs:
    """This class contains all the urls that are used to make requests to the API

    Don't use it.
    """

    def __init__(self):
        self.base_url = "https://tl3.shadowtree-software.se/TL3BackEnd/rest/"

        self.user_search_base = "user2/public/search?query="
        self.user_info_base = "user2/public/info/"
        self.map_base = "map/public/"

url = URLs()

def user_search(name):
    """This function returns the data from the user search API in a form of a JSON/Python dictionary
    """
    link = url.base_url + url.user_search_base + str(name)
    result = requests.get(link, verify = False).json()
    if not len(result):
        raise KeyError("No user with such a name exists!")
    return result

def user_info(id):
    """This function returns the data from the user info API in a form of a JSON/Python dictionary
    """
    link = url.base_url + url.user_info_base + str(id)
    result = requests.get(link, verify = False).json()
    if not len(result):
        raise KeyError("No user with such an id exists!")
    return result

def map_top(mode, time, trendsystem):
    """This function returns the data from the top maps API in a form of a JSON/Python dictionary
    """
    link = url.base_url + url.map_base + f"top/{str(mode)}/{str(time)}?maxversion=999&trendsystem={trendsystem}"
    result = requests.get(link, verify = False).json()
    return result

def map_user(id, resultsPerPage, page):
    """This function returns the data from the user maps API in a form of a JSON/Python dictionary
    """
    link = url.base_url + url.map_base + f"user/{str(id)}?result={resultsPerPage}&page={page}"
    result = requests.get(link, verify = False).json()
    return result