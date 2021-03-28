from typing import Optional, Any, Dict

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from httpx import Client, HTTPStatusError

from olxbrasil.constants import CATEGORIES
from olxbrasil.exceptions import OlxRequestError
from olxbrasil.filters import Filter, LocationFilter
from olxbrasil.parsers import ListParser, ItemParser


class Olx:
    def __init__(
        self,
        *,
        category: str,
        subcategory: Optional[str] = None,
        location: Optional[LocationFilter] = None,
        filters: Optional[Filter] = None,
    ):
        if not location:
            self.__location = None
            self.__subdomain = "www"
        else:
            self.__location = location
            self.__subdomain = self.__location.state.lower()
        self.__user_agent = UserAgent()
        self.__category = None
        self.__subcategory = None
        self._client = Client(
            base_url=f"https://{self.__subdomain}.olx.com.br",
            headers={"User-Agent": self.__user_agent.random},
        )
        self.__filters = filters

        valid_category = category in CATEGORIES.keys()

        if valid_category:
            valid_subcategory = (
                subcategory in CATEGORIES[category]["subcategories"].keys()
            )
            self.__category = CATEGORIES[category]["category"]

            if subcategory and valid_subcategory:
                sub = CATEGORIES[category]["subcategories"][subcategory]
                self.__subcategory = sub

            if subcategory and not valid_subcategory:
                raise ValueError(
                    f"{subcategory} is not a valid subcategory, please provide a valid subcategory: "
                    f"{' '.join(CATEGORIES[category]['subcategories'].keys())}"
                )
        else:
            raise ValueError(
                f"{category} is not a valid category, please provide a valid category: "
                f"{' '.join(CATEGORIES.keys())}"
            )

    def __build_url(self):
        url = ""
        if self.__location:
            url += self.__location.get_endpoint()

        url += f"/{self.__category}"

        if self.__subcategory:
            url += f"/{self.__subcategory}"

        if self.__filters:
            url += self.__filters.get_endpoint()

        return url

    def get_all(self, page=0) -> Dict[str, Any]:
        parameters = {"o": min(page, 100)}
        url = self.__build_url()

        if self.__filters:
            parameters = self.__filters.get_filters(parameters)

        try:
            response = self._client.get(url, params=parameters)

            response.raise_for_status()
        except HTTPStatusError:
            raise OlxRequestError("Was not possible to reach OLX server")

        soup = BeautifulSoup(response.text, "html.parser")

        parser = ListParser(soup)

        return parser.items

    def get_item(self, url: str) -> ItemParser:
        response = self._client.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        parser = ItemParser(soup)
        return parser
