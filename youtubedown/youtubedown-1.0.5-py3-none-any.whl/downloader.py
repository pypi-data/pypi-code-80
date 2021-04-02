import re
from youtubedown.module1 import asyncmodule


class asyncDown():
    def __init__(self, title: str, path:str, check):
        self.title = title
        self.check = check
        self.path = path

    async def lookup(path: str=None , title: str=None):
        if not path: 
            path = "music"
        else:
            pass
        URL_REGEX = re.compile(
            r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
        )
        
        if URL_REGEX.match(title):
            title_url= True
        else:
            title_url = False
        return asyncDown(title=title, check=title_url, path=path)
    async def download(self):
        if self.check is None: return {"result": None}
        if self.check is True:
            result = await asyncmodule.urldown(self, nick=self.path, title=self.title)
            return result
        if self.check is False:
            result = await asyncmodule.titledown(self, nick=self.path, title=self.title)
            return result
    async def search(self):
        if self.check is None: return {"result": None}
        if self.check is True:
            result = await asyncmodule.urlsearch(self, title=self.title)
            return result
        if self.check is False:
            result = await asyncmodule.titleserach(self, title=self.title)
            return result