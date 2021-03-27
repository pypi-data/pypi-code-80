###############################################################################
# Module Imports
###############################################################################

import scpper.utils

try:
    from collections.abc import namedtuple
except ImportError:
    from collections import namedtuple
import json

###############################################################################
# API Classes
###############################################################################

class Scpper:

    """Scpper API wrapper class

    Attributes:
        site: Branch site name.
            SCP Foundation (scp-wiki.net): "en"
            Russian branch (scpfoundation.ru): "ru"
            Korean branch (ko.scp-wiki.net): "ko"
            Japanese branch (ja.scp-wiki.net): "ja"
            French branch (fondationscp.wikidot.com): "fr"
            Spanish branch (lafundacionscp.wikidot.com): "es"
            Thai branch (scp-th.wikidot.com): "th"
            Polish branch (scp-wiki.net.pl): "pl"
            German branch (scp-wiki-de.wikidot.com): "de"
            Chinese branch (scp-wiki-cn.wikidot.com): "cn"
            Italian branch (fondazionescp.wikidot.com): "it"
            SCP International (scp-int.wikidot.com): "int"
    """

    ###########################################################################
    # Special Methods
    ###########################################################################

    def __init__(self,site="en"):
        self.site = site
        self.req = scpper.utils.InsistentRequest()
    
    def __repr__(self):
        return '{}.{}({})'.format(
            self.__module__,
            self.__class__.__name__,
            repr(self.site))

    ###########################################################################
    # Public Methods
    ###########################################################################

    def find_pages(self, title, limit=50, random=0):

        """Retrieves up to limit pages from the specified wiki with part of the name matching title.

        Args:
            site: 
                Short name from the list of available sites (see below)
            title: 
                Search query, part of page's name (i.e. "173" will match "SCP-173", "SCP-1173", etc). Between 3 and 256 characters.
            limit: 
                Maximum number of rows returned by the query. Limited to 50.
            random: 
                Bit flag indicating whether resulting list of pages should be randomized.
                "0" - returns limit pages ordered by (kind of) relevance, descending (default)
                "1" - returns random selection of limit pages from the original query.

        Returns:
            A list object containing all found pages.

        Raises:
            ValueError: Title must be between 3 and 256 characters long.
        """

        if len(title) < 3 or len(title) > 256:
            raise ValueError("Title must be between 3 and 256 characters long")

        res = self.req.get(f"http://scpper.com/api/find-pages",
            params={"site": self.site,
            "title": title,
            "limit": limit,
            "random": random
            })
        pages = json.loads(res.text)["pages"]

        return [Page(page["id"]) for page in pages]

    def find_users(self, name, limit=50):

        """Retrieves up to limit users from the with part of the name matching name.

        Args:
            site: 
                Optional. Short name from the list of available sites (see below). If specified, only searches amongst members of the site. Otherwise - amongst all users.
            name: 
                Search query, part of user's name (i.e. "cle" will match "Dr Clef", "Agent MacLeod", etc). Between 3 and 256 characters.
            limit: 
                Maximum number of rows returned by the query. Limited to 50.

        Returns:
            A list object containing all found users.

        Raises:
            ValueError: Name must be between 3 and 256 characters long.
        """

        if len(name) < 3 or len(name) > 256:
            raise ValueError("Name must be between 3 and 256 characters long")

        res = self.req.get(f"http://scpper.com/api/find-users",
            params={"site": self.site,
            "name": name,
            "limit": limit
            })
        users = json.loads(res.text)["users"]

        return [User(user["id"]) for user in users]

    def tags(self, method, tags, limit=50, random=0):

        """Retrieves up to limit pages from the specified wiki, selected using provided tags.

        Args:
            site: 
                Short name from the list of available sites (see below)
            method: 
                How to combine provided tags for the query ("and"/"or")
                "and" - only pages that have all the tags (default)
                "or" - pages that contain any of the tags.
            tags: 
                List of tags, each prefixed with "+" or "-", separated by commas
                "+" indicates that pages containing this tag must be included in the query
                "-" indicates that pages containing this tag must be excluded from the query
                Each tag MUST be prefixed by only ONE of those options.
            limit: 
                Maximum number of rows returned by the query. Limited to 50.
            random: 
                Bit flag indicating whether resulting list of pages should be randomized.
                "0" - returns limit pages ordered by clean rating, descending (default)
                "1" - returns random selection of limit pages from the original query.

        Returns:
            A list object containing all selected pages.
        """

        res = self.req.get(f"http://scpper.com/api/tags",
            params={"site": self.site,
            "method": method,
            "tags": tags,
            "limit": limit,
            "random": random
            })
        pages = json.loads(res.text)["pages"]
      
        return [Page(page["id"]) for page in pages]

class Page:

    """Scpper page class

    Attributes:
        id: Wikidot id of the page to retrieve.
    """

    ###########################################################################
    # Special Methods
    ###########################################################################
    
    def __init__(self, id):
        self.id = id
        self.req = scpper.utils.InsistentRequest()

    def __repr__(self):
        return '{}.{}({})'.format(
            self.__module__,
            self.__class__.__name__,
            repr(self.id))

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def _data(self):

        """Retrieves a page data by id.
        
        Args:
            none

        Returns:
            A dict object containing a page metadata.

        Raises:
            scpper.utils.NotFoundException: Page not found.
        """
        
        res = self.req.get(f"http://scpper.com/api/page", 
            params={'id': self.id})
        data = json.loads(res.text)
        if "error" in data:
            raise scpper.utils.NotFoundException(data["error"])
        else:
            return data

    @property
    def site(self):
        return self._data["site"]

    @property
    def name(self):
        return self._data["name"]

    @property
    def title(self):
        return self._data["title"]

    @property
    def altTitle(self):
        return self._data["altTitle"]
    
    @property
    def status(self):
        return self._data["status"]

    @property
    def kind(self):
        return self._data["kind"]

    @property
    def creationDate(self):
        return self._data["creationDate"]

    @property
    def rating(self):
        return self._data["rating"]

    @property
    def cleanRating(self):
        return self._data["cleanRating"]

    @property
    def contributorRating(self):
        return self._data["contributorRating"]

    @property
    def adjustedRating(self):
        return self._data["adjustedRating"]

    @property
    def wilsonScore(self):
        return self._data["wilsonScore"]

    @property
    def rank(self):
        return self._data["rank"]

    @property
    def authors(self):
        return self._data["authors"]

    @property
    def deleted(self):
        return self._data["deleted"]

class User:

    """Scpper user class

    Attributes:
        id: Wikidot id of the user to retrieve.
    """

    ###########################################################################
    # Special Methods
    ###########################################################################
    
    def __init__(self, id):
        self.id = id
        self.req = scpper.utils.InsistentRequest()

    def __repr__(self):
        return '{}.{}({})'.format(
            self.__module__,
            self.__class__.__name__,
            repr(self.id))

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def _data(self):

        """Retrieves a user data by id.
        
        Args:
            none

        Returns:
            A dict object containing a user metadata.

        Raises:
            scpper.utils.NotFoundException: User not found.
        """

        res = self.req.get(f"http://scpper.com/api/user", 
            params={'id': self.id})
        data = json.loads(res.text)
        if "error" in data:
            raise scpper.utils.NotFoundException(data["error"])
        else:
            return data

    @property
    def name(self):
        return self._data["name"]

    @property
    def displayName(self):
        return self._data["displayName"]

    @property
    def deleted(self):
        return self._data["deleted"]

    @property
    def activity(self):
        activity = {}
        for branch in self._data["activity"]:
            activity[branch] = Activity(self._data["activity"][branch]["votes"],
                self._data["activity"][branch]["revisions"],
                self._data["activity"][branch]["pages"],
                self._data["activity"][branch]["lastActive"],
                self._data["activity"][branch]["member"],
                self._data["activity"][branch]["highestRating"],
                self._data["activity"][branch]["totalRating"],
                )
        return activity

###############################################################################
# Named Tuple Containers
###############################################################################

nt = namedtuple
Activity = nt("Activity", "votes revisions pages lastActive member highestRating totalRating")
del nt