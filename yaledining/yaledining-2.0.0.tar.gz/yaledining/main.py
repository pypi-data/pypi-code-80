import requests
import datetime
from unidecode import unidecode
from .models import *


class ConnectionError(Exception):
    """Raised when an error occurs in connecting to the API."""
    pass


class YaleDining:
    def __init__(self):
        raise Exception('The YaleDining class has been deprecated in v2.0 of this package. Use API instead.')


class API:
    API_ROOT = 'https://yaledine.com/api/'
    DATE_FMT = '%Y-%m-%d'

    def _get(self, endpoint: str, params: dict = {}, json=True):
        """
        Make a GET request to the API.

        :param endpoint: path to resource desired.
        :param params: dictionary of custom params to add to request.
        """
        request = requests.get(self.API_ROOT + endpoint, params=params)
        if request.ok:
            return request.json()
        else:
            raise ConnectionError('API request failed.')

    def _date(self, raw):
        if type(raw) == str:
            return raw
        if type(raw) in (datetime.date, datetime.datetime):
            return raw.strftime(self.DATE_FMT)
        return None

    def halls(self):
        """
        Get all halls available from the API.
        """
        return [Hall(raw, self) for raw in self._get('halls')]

    def hall(self, id: str):
        """
        Get a single dining hall by ID.
        :param id: ID (two-letter abbreviation) of the hall you want.
        """
        return Hall(self._get(f'halls/{id}'), self)

    def hall_managers(self, hall_id: str):
        """
        Get managers for a dining hall.
        :param hall_id: ID (two-letter abbreviation) of the hall you want managers for.
        """
        return self.managers(hall_id)

    def hall_meals(self, hall_id: str, *args, **kwargs):
        """
        Get meals for a given hall. Accepts same parameters as meals.
        :param hall_id: ID (two-letter abbreviation) of hall for which to get menus.
        """
        return self.meals(hall_id, *args, **kwargs)

    def managers(self, hall_id: str = None):
        """
        Get managers for a given hall, or all managers if hall_id is omitted.
        :param hall_id: ID (two-letter abbreviation) of hall for which to get managers.
        """
        endpoint = f'halls/{hall_id}/managers' if hall_id else 'managers'
        return [Manager(raw, self) for raw in self._get(endpoint)]

    def meals(self, hall_id: str = None, date=None, start_date=None, end_date=None):
        """
        Get meals for a given hall (or all halls if hall_id is omitted), for a given date or within a range.
        :param hall_id: ID (two-letter abbreviation) of hall for which to get menus.
        :param date: single date to get meals for. Can be YYYY-MM-DD string or datetime.date.
        :param start_date: start of date range to get meals for. Ignored if date is passed. Can be YYYY-MM-DD string or datetime.date.
        :param end_date: end of date range to get meals for. Ignored if date is specified. Can be YYYY-MM-DD string or datetime.date.
        """
        endpoint = f'halls/{hall_id}/meals' if hall_id else 'meals'
        params = {}
        if date:
            params['date'] = self._date(date)
        elif start_date and end_date:
            params['startDate'] = self._date(start_date)
            params['endDate'] = self._date(end_date)
        return [Meal(raw, self) for raw in self._get(endpoint, params=params)]

    def meal(self, id: int):
        """
        Get a single meal by ID.
        :param id: ID of meal to get.
        """
        return Meal(self._get(f'meals/{id}'), self)

    def meal_items(self, meal_id: int):
        """
        Get items in a given meal.
        :param meal_id: ID of meal to get items for.
        """
        return self.items(meal_id)

    def items(self, meal_id: int = None):
        """
        Get all items served.
        """
        endpoint = f'meals/{meal_id}/items' if meal_id else 'items'
        return [Item(raw, self) for raw in self._get(endpoint)]

    def item(self, id: int):
        """
        Get a single item.
        :param id: ID of item to get.
        """
        return Item(self._get(f'items/{id}'), self)

    def item_nutrition(self, item_id: int):
        """
        Get nutrition data for a menu item.
        :param item_id: ID of item to get nutrition data for.
        """
        return Nutrition(self._get(f'items/{item_id}/nutrition'), self)
