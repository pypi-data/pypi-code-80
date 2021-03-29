"""Centralized methods to work with Redis."""
import logging

import redis

logger = logging.getLogger(__name__)


class Redis(object):
    """Push and pull data form a redis key value datastore."""

    def __init__(self, redis_password, host, port=6379):
        """Create a redis datastore.

        :param redis_password: Password of redis store.
        :type redis_password: str
        :param host: Hostname where redis runs.
        :type host: str
        :param port: Port on which redis runs.
        :type port: int
        """
        self.store = redis.StrictRedis(
            host=host,
            port=port,
            password=redis_password
        )

    def get_all_matching_items(self, key_match="*"):
        """Get the newest fid from the redis queue.

        Example use:
            get_all_matching_items(
                key_match="document_*"
            )

        :param key_match: regex type string to match keys in store
          By default "*" selects from all items in store.
        :type key_match: str
        :return: All items in store that match the key_match
        :rtype: list
        """
        all_matching_keys = [bk.decode("utf-8") for bk
                             in self.store.keys(key_match)]
        logger.debug(
            "found {} items in store with match '{}'".format(
                len(all_matching_keys),
                key_match
            )
        )
        if len(all_matching_keys) == 0:
            return []

        all_values = [bv.decode("utf-8") if bv else '' for bv
                      in self.store.mget(all_matching_keys)]

        all_matching_items = []

        # noinspection PyTypeChecker
        for i in range(len(all_matching_keys)):
            all_matching_items.append({
                'key': all_matching_keys[i],
                'value': all_values[i]
            })
        return all_matching_items

    def get_first_item(self, key_match="*", sort_function=None, reverse=True):
        """Get the newest fid from the redis queue.

        Example use:
            get_first_val(
                key_match="document_*",
                sort_function=lambda x: str(x).split("_")[1],
                reverse=True
            )

        :param key_match: regex type string to match keys in store
          By default "*" selects from all items in store.
        :type key_match: str
        :param sort_function: Function to apply to sorting function.
          If None, then sorting will be done staight on the input without
          any transformation.
        :type sort_function: function
        :param reverse: True if sorted list should be reversed.
          By default is set to True, thus largest value is first.
          Done with assumption that datetime is in key.
        :type reverse: bool
        :return: First key and value pair or None if queue is empty
        :rtype: dict or None
        """
        logger.debug("getting '{}' from store".format(key_match))
        all_matching_keys = self.store.keys(key_match)
        logger.debug(
            "found {} items in store with match '{}'".format(
                len(all_matching_keys),
                key_match
            )
        )

        if len(all_matching_keys) == 0:
            return None

        if not sort_function:
            def sort_function(invar):
                """Default sorting function that does nothing.

                :param invar: input var
                :type invar: Any
                :return: output to get sorted
                :rtype: Any
                """
                return invar

        sorted_keys = sorted(
            all_matching_keys,
            key=sort_function,
            reverse=reverse
        )

        first_key = sorted_keys[0].decode("utf-8")
        logger.debug("First_key = '{}'".format(first_key))

        first_val = self.store.get(first_key).decode("utf-8")
        logger.debug("first_val = '{}'".format(first_val))

        return {
            'key': first_key,
            'value': first_val
        }

    def pop_first_val(self, key_match="*", sort_function=None, reverse=True):
        """Get the newest fid from the redis queue and then remove it.

        Example use:
            pop_first_val(
                key_match="document_*",
                sort_function=lambda x: str(x).split("_")[1],
                reverse=True
            )

        :param key_match: regex type string to match keys in store
          By default "*" selects from all items in store.
        :type key_match: str
        :param sort_function: Function to apply to sorting function.
          If None, then sorting will be done staight on the input without
          any transformation.
        :type sort_function: function
        :param reverse: True if sorted list should be reversed.
          By default is set to True, thus largest value is first.
          Done with assumption that datetime is in key.
        :type reverse: bool
        :return: First key and value pair or None if empty
        :rtype: dict or None
        """
        first_item = self.get_first_item(
            key_match=key_match,
            sort_function=sort_function,
            reverse=reverse
        )
        if not first_item:
            return None

        first_key = first_item['key']
        first_val = first_item['value']

        self.store.delete(first_key)
        logger.debug("removed '{}' from queue".format(first_key))

        return {
            'key': first_key,
            'value': first_val
        }

    def add_to_store(self, key, value):
        """Add the value to a redis queue.

        Example use:
            add_to_store(
                key="example_key_123",
                value="key_value"
            )

        :param key: key value of item in store
        :type key: str
        :param value: value of item in datastore
        :type value: str
        :return: None
        :rtype: None
        """
        self.store.set(key, value)
        logger.debug("added to redis:  '{}':'{}'".format(key, value))
