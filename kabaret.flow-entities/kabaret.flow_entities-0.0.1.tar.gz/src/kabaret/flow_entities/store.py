import pprint

import pymongo

from kabaret import flow


class Storable(object):
    """
    Class Mixin for all things needing access to the entity store.

    This needs the `self.root().project().get_entity_store() to be
    implemented to return a `kabaret.flow_entities.store.EntityStore`
    instance.
    """

    def get_entity_store(self):
        return self.root().project().get_entity_store()


class TestConnectionAction(flow.Action):

    _store = flow.Parent()

    def needs_dialog(self):
        return True

    def get_buttons(self):
        self.message.set("Clik the button to test the connection.")
        return ["Test"]

    def run(self, button):
        try:
            info = self._store.get_db_info()
        except Exception as err:
            self.message.set(
                "<font color=red>Connection error:</font><br>"
                "<pre>{}</pre>".format(err)
            )
        else:
            self.message.set(
                "Connection looks <b>OK</b>.<br>" "See console output for details."
            )
            pprint.pprint(info)
        return self.get_result(close=False)


class EntityStore(flow.Object):

    DEFAULT_URI = "mongodb://localhost:27017/?connect=true&w=majority"
    uri = flow.Param(DEFAULT_URI).ui(
        tooltip="Must look like: "
        "<b>mongodb[+srv]://[{login}:{password}]@{host}[:{port}]/[{default_db_name}]"
        "?connect=true&w=majority</b>",
    )
    test_connection = flow.Child(TestConnectionAction)

    def __init__(self, *args, **kwargs):
        super(EntityStore, self).__init__(*args, **kwargs)
        self._mongo_client = None

    def ensure_connected(self):
        if self._mongo_client is None:
            uri = self.uri.get().strip()
            appname = self.root().session().session_uid()
            self._mongo_client = pymongo.MongoClient(
                uri,
                appname=appname,
            )

    def _client(self):
        self.ensure_connected()
        return self._mongo_client

    def get_db_info(self):
        info = self._client().server_info()
        return info

    def get_collection(self, collection_name):
        self.ensure_connected()
        cluster_name = self.root().session().cmds.Cluster.get_cluster_name()
        db = self._client()[cluster_name]
        return db[collection_name]

    def ensure_index(self, collection_name, specs, **options):
        self.get_collection(collection_name).create_index(specs, **options)
