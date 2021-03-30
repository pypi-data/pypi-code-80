#!/usr/bin/env python
from acme_news.browser.acme_browser import ACMEBrowser
from typing import List, Dict

class RussiaToday(ACMEBrowser):

    def __init__(self, query: str,
                 category: str = "politics",
                 content_type: str = "News"):
        """
        DESCRIPTION
            Helper class to collect the contents from Russia Today

        PARAMETERS
            :param query:
            :param category:
            :param content_type:

        FUNCTIONS
            __init__
            __build_search_query__
            parse_rt_contents
        """
        self.search_query: str = ""
        if not query:
            raise ValueError("Please provide a valid query.")

        self.rt_url: str = "https://www.rt.com/search"
        self.extra_query_params: str = ""
        self.rt_driver = None
        self.query: str = query
        self.category: str = category
        self.content_type: str = content_type
        self.__build_search_query__()
        super(RussiaToday, self).__init__()

    def __set_extra_params__(self, page_size: int, page: int):
        if not all([page, page_size]) and (page <= 0 and page_size <= 0):
            raise ValueError("Please provide the right values for page and the page_size")

        self.extra_query_params = f"&pageSize={page_size}&format=&page={page}"

    def __get_extra_params__(self):
        return f"{self.search_query}{self.extra_query_params}"

    def __build_search_query__(self):
        self.search_query = f"{self.rt_url}?q={self.query}&type={self.content_type}&xcategory={self.category}"

    def parse_rt_contents(self) -> List[Dict]:
        results: List = []
        self.rt_driver = self.browser(url=self.search_query)
        rt_response = self.rt_driver.find_element_by_class_name("news-block").find_element_by_class_name('card-list').find_elements_by_css_selector('li.card-list__item')

        for element in rt_response:
            try:
                summary = element.find_element_by_css_selector('div.card__summary')
                current_article: Dict = {
                    'region_name': self.query,
                    'url': summary.find_element_by_css_selector('a.link').get_attribute('href'),
                    'title': element.find_element_by_css_selector('strong.card__header.card__header_serp-list').text,
                    'news_date': element.find_element_by_css_selector('time.date').text,
                    'category': self.category,
                    'summary': summary.text
                }
                results.append(current_article)
            except:
                pass

        self.rt_driver.close()
        return results

    def rt_bulk_quries(self, page: int, page_size: int) -> List[Dict]:
        self.__set_extra_params__(page_size=page_size, page=page)

        results: List = []
        self.rt_driver = self.browser(url=self.__get_extra_params__())

        rt_response = self.rt_driver.find_elements_by_class_name("news-block")
        if not rt_response:
            raise ConnectionError(f"Unable to parse the contents from RT {self.__get_extra_params__()}")

        for content in rt_response:
            try:
                contents = content.find_element_by_class_name('card-list').find_elements_by_css_selector('li.card-list__item')
                for element in contents:
                    card = element.find_element_by_css_selector('div.card')

                    contents: Dict = {
                        'region_name': self.query,
                        'url': card.find_element_by_css_selector('a.link.link_hover').get_attribute('href'),
                        'title': card.find_element_by_css_selector('a.link.link_hover').text,
                        'category': self.category,
                        'content': card.text,
                        'image_url': card.find_element_by_css_selector('img.media__item.media__item_ratio').get_attribute('src'),
                        'date': card.find_element_by_css_selector('time.date').text
                    }
                    results.append(contents)
            except:
                pass

        self.rt_driver.close()
        return results
