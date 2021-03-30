import time

from kabaret import flow

from .utils import isidentifier, identifier_param_split
from .store import Storable


class PropertyValue(flow.values.Value):

    _entity = flow.Parent()

    def set(self, value):
        self._entity.set_property(self.name(), value)
        self.touch()
        self.notify()

    def get(self):
        return self._entity.get_property(self.name())


class Property(flow.Param):
    def __init__(self, property_value_type=None):
        property_value_type = property_value_type or PropertyValue
        super(Property, self).__init__("", property_value_type)
        self.watched(True)


class Entity(flow.Object):
    """
    Subclass this to create your entities.

    Use Propery relations to add queryable
    properties in your entities.

    You can also use classic Relation, but
    those won't be usable in query filters.
    """

    _collection = flow.Parent()

    @classmethod
    def get_property_names_and_labels(cls):
        return [("name", "Name")] + [
            (
                relation.name,
                relation.get_ui().get("label")
                or relation.name.replace("_", " ").title(),
            )
            for relation in cls._relations
            if isinstance(relation, Property)
        ]

    def set_property(self, property_name, value):
        self._collection.set_property(self.name(), property_name, value)

    def get_property(self, property_name):
        return self._collection.get_property(self.name(), property_name)

    def child_value_changed(self, child_value):
        self.touch()
        self._collection.touch()


class CreateEntitiesAction(flow.Action):

    _collection = flow.Parent()

    entity_names = flow.Param().ui(
        tooltip="Names of Entities to create, separated by spaces."
    )

    def needs_dialog(self):
        return True

    def get_buttons(self):
        self.message.set(
            "Enter entity names, separated with a space<br>"
            "Valid names must start by a letter and contain only "
            'letters, digits, "_", and must not be python keywords.'
        )
        return ["Create"]

    def run(self, button):
        valid_names, invalid_names = identifier_param_split(self.entity_names.get())
        self._collection.ensure_exist(valid_names)
        if invalid_names:
            self.entity_names.set(invalid_names)
            self.message.set(
                "Created {} entities<br>"
                "Those are <b>not valid</b> entity names:".format(len(valid_names))
            )
        else:
            self.message.set("Created {} entities<br>".format(valid_names))
        self._collection.touch()
        return self.get_result(close=False)


class DeleteEntitiesAction(flow.Action):

    MSG = (
        'Enter "Confirm !" in the confirmation field '
        'and click "Delete Forever"<br>'
        "<h2><font color=red>NO POSSIBLE UNDO FOR THIS !</font></h2>"
    )

    _collection = flow.Parent()

    entity_names = flow.Param("")
    confirmation = flow.Param("")

    def needs_dialog(self):
        return True

    def get_buttons(self):
        self.confirmation.set("")
        self.message.set(self.MSG)
        return ["Delete Forever"]

    def run(self, button):
        if button != "Delete Forever":
            self.message.set("<br>!!! WRONG BUTTON !!!<br>" + self.MSG)
            return self.get_result(close=False)

        if self.confirmation.get() != "Confirm !":
            self.message.set("<br>NOT CONFIRMED !!!<br>" + self.MSG)
            return self.get_result(close=False)

        valid_names, invalid_names = identifier_param_split(self.entity_names.get())
        if invalid_names:
            self.message.set(
                "!!! NOT A NAMES ARE VALID !!!<br>"
                "invalids: " + " ".join(invalid_names) + "<br>" + self.MSG
            )

        self._collection.delete_entities(valid_names)
        self._collection.touch()
        self.entity_names.set("")
        self.confirmation.set("")
        self.message.set("Deleted {} entities".format(len(valid_names)))
        return self.get_result(close=False)


class EntityCollection(flow.DynamicMap, Storable):
    """
    Subclass and override `mapped_type(cls)` to
    define an entity collection in your flow.
    """

    @classmethod
    def mapped_type(cls):
        return Entity

    def __init__(self, *args, **kwargs):
        self._index_ensured = False
        self._document_cache = None
        self._document_names_cache = None
        self._document_cache_ttl = 5  # seconds before invalidating the cache
        self._document_cache_birth = None
        self._document_cache_key = None

        super(EntityCollection, self).__init__(*args, **kwargs)

    def __len__(self):
        collection = self.get_entity_store().get_collection(self.collection_name())
        q = self.query_filter()
        if not q:
            return collection.count()
        return collection.find(self.query_filter()).count()

    def collection_name(self):
        """
        You can override this and point to another
        collection in the db to share entities with another
        collection.

        (Entities properties do not *need* to match but beware
        that the db will store both property lists)
        """
        return "{}/{}".format(self.oid(), self.mapped_type().__name__)

    def ensure_indexes(self):
        if self._index_ensured:
            return
        self.get_entity_store().ensure_index(
            self.collection_name(),
            [("name", 1)],
            unique=True,
        )
        # TODO: also add index from Entity Properties here.
        self._index_ensured = True

    def query_filter(self):
        """
        You can override this to provide a query filter.

        for example:
            return {"status": "WIP"}

        see https://docs.mongodb.com/manual/tutorial/query-documents/
        """
        return {}

    def set_property(self, entity_name, property_name, value):
        self.get_entity_store().get_collection(self.collection_name()).update_one(
            {"name": entity_name},
            {"$set": {property_name: value}},
        )

    def get_property(self, entity_name, property_name):
        print("===========>", entity_name, property_name)
        value = (
            self.get_entity_store()
            .get_collection(self.collection_name())
            .find_one(
                {"name": entity_name},
                {property_name: 1},
            )
        )
        try:
            return value[property_name]
        except KeyError:
            default = getattr(self.mapped_type(), property_name).get_default_value()
            return default

    def mapped_names(self, page_num=0, page_size=None):
        cache_key = (page_num, page_size)
        if (
            self._document_cache is None
            or self._document_cache_key != cache_key
            or self._document_cache_birth < time.time() - self._document_cache_ttl
        ):
            cursor = (
                self.get_entity_store()
                .get_collection(self.collection_name())
                .find(self.query_filter())
            )
            if page_num is not None and page_size is not None:
                cursor.skip((page_num - 1) * page_size)
                cursor.limit(page_size)
            name_and_doc = [(i["name"], i) for i in cursor]
            self._document_names_cache = [n for n, d in name_and_doc]
            self._document_cache = dict(name_and_doc)
            self._document_cache_birth = time.time()
            self._document_cache_key = cache_key
            self.ensure_indexes()

        return self._document_names_cache

    def touch(self):
        self._document_cache = None
        super(EntityCollection, self).touch()

    def columns(self):
        return [
            label for name, label in self.mapped_type().get_property_names_and_labels()
        ]

    def _fill_row_cells(self, row, item):
        if self._document_cache is None:
            # trigger a cache update:
            # FIXME: this cache update is not paginated :'(
            self.mapped_names()
        entity_name = item.name()
        for name, label in self.mapped_type().get_property_names_and_labels():
            row[label] = self._document_cache[entity_name].get(name, "")

    def ensure_exist(self, entity_names):
        self.get_entity_store().get_collection(self.collection_name()).insert_many(
            [{"name": name} for name in entity_names]
        )

    def delete_entities(self, entity_names):
        collection = self.get_entity_store().get_collection(self.collection_name())
        for name in entity_names:
            collection.delete_one({"name": name})
