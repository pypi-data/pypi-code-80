"""Create and manage documents.

A document is any object that has text properties.  We process documents by
indexing directly to Solr.
In future can marshall the document into pubsub etc from here.
"""
import json
import logging

from modsolr import Solr

logger = logging.getLogger(__name__)


class Document(object):
    """Create the document base class which defines how we deal with it."""

    class Meta:
        """Abstract document does not get instantiated."""
        abstract = True

    def __init__(self):
        """Instantiate the Document class."""
        pass

    def index_to_solr(self, collection, solr_url):
        """Index json object string in solr format to Solr.

        NOTE: This treats all attributes as dynamic fields.

        :param collection: Solr collection where data sits.
        :type collection: str
        :param solr_url: Solr Url where collection sits
        :type solr_url: str
        :return: None
        :rtype: None
        """
        self.index_dict_to_solr(self.solr_serialize(), collection, solr_url)

    @staticmethod
    def index_dict_to_solr(doc, collection, solr_url):
        """Index json object string in solr format to Solr.

        :param doc: The data to be indexed to solr
        :type doc: dict
        :param collection: Solr collection where data sits.
        :type collection: str
        :param solr_url: Solr Url where collection sits
        :type solr_url: str
        :return: None
        :rtype: None
        """
        solr = Solr(collection, solr_url)
        doc = json.dumps(doc)

        solr.update_by_json(doc, commit=True)

    @staticmethod
    def add_to_solr_index(doc_list, collection, solr_url, id_field="id"):
        """Add to Solr index by adding a list of dicts.

        :param doc_list: A list of solr compatable dicts.
        :type doc_list: list of dict
        :param collection: Solr collection where data sits.
        :type collection: str
        :param solr_url: Solr Url where collection sits
        :type solr_url: str
        :param id_field: name of id field, which identifies the solr document.
        :type id_field: str
        :return: None
        :rtype:None
        """
        solr = Solr(collection, solr_url)

        # create rules for adding
        keywords = list(doc_list[0].keys())
        keywords.remove(id_field)
        keyword_arg = {s: "add" for s in keywords}

        solr.update_docs(
            doc_list,
            commit=True,
            **keyword_arg
        )

    # noinspection PyDefaultArgument
    def solr_serialize(self, dynamic_fields=None, static_fields=["id"]):
        """Convert the instance attributes to a dictionary as needed by Solr.

        :param dynamic_fields: All keys that we want to serialize
          If left None, then it takes all.
        :type dynamic_fields: list of str
        :param static_fields: Fields that should be passed as-is to Solr.
          For example, the id field should not be changed to id_s
        :type static_fields: list of str
        :return: Dict representation of instance properties.
        :rtype: dict
        """
        ret = {}
        # Static fields go in as-is
        for key in static_fields:
            ret[key] = self.__dict__[key]

        # if Non dynamic fields defined, then add all of them
        if dynamic_fields is None:
            dynamic_fields = self.__dict__.keys()

        # go through each attribute of self and seralize desired and possible
        for key, val in self.__dict__.items():
            # skip item if value is empty or not desired
            if val is None or val == [] or key not in dynamic_fields:
                continue

            # Check if value is serializable (after values have been mapped)
            try:
                _ = json.dumps(val)
            except TypeError:
                # value is not serializable, so skip it.
                logger.debug(
                    "'{}':{} is not json seralizable".format(key, val))
                continue

            (key, val) = self.solr_serialize_item(key, val)

            ret[key] = val

        return ret

    @staticmethod
    def solr_serialize_item(key, val):
        """Serialize a single item.

        :param key: The key in solr that will get its type appended.
        :type key: str
        :param val: The value, which defines the key change.  May change
        :type val: Any
        :return: Solr serialized key, value pair
        :rtype: tuple
        """
        # else check each value type and modify as required
        if isinstance(val, list):
            # multivalued field
            pairs = [Solr.solr_type_serializer(key, v) for v in val]
            key = "{}s".format(pairs[0][0])  # key is always the same
            val = [t[1] for t in pairs]  # need each serialized val
        else:
            # single valued field
            key, val = Solr.solr_type_serializer(key, val)

        return key, val
