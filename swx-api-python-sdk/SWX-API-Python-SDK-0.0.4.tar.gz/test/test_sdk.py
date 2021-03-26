"""Module to test PythonApiClient"""

from os import environ
import unittest
import pytest
import swx_sdk
from swx_sdk.swx_api_client import SwxApiClient
from swx_sdk.api import collections_api
from swx_sdk.model.collection_request import CollectionRequest
from swx_sdk.model.collection_update_request import CollectionUpdateRequest
from swx_sdk.api import models_api
from swx_sdk.model.model_request import ModelRequest
from swx_sdk.model.model_update_request import ModelUpdateRequest
from swx_sdk.api import things_api
from swx_sdk.model.thing_request import ThingRequest
from swx_sdk.model.thing_update_request import ThingUpdateRequest


# initialize variables or read from environment
pytest.client_id = environ.get('client_id', None).strip()
pytest.client_secret = environ.get('client_secret', None).strip()
pytest.scope = environ.get('scope', None).strip()                   # "collection data label thing model"
pytest.space = environ.get('space', None).strip()
pytest.host = environ.get('swx_host', None).strip()

pytest.THING_ID = ""
COLLECTION_NEW = 'collnew1'
THING_TITLE_NEW = 'thingnew1'
MODEL_NAME_NEW = 'modelnew1'

class ClientAPIInstance():
    """ClientAPIInstance creates environment based instance of API client"""

    def __init__(self):

        self.client_id = pytest.client_id
        self.client_secret = pytest.client_secret
        self.scope = pytest.scope
        self.host = pytest.host
        self.configuration = swx_sdk.Configuration(
            host=pytest.host
        )

        if environ.get('verify_ssl', True) in ['False', 'false']:
            self.configuration.verify_ssl = False

    def get_swxclient(self):
        client_id = self.client_id
        client_secret = self.client_secret
        scope = self.scope
        defer_auth = False

        """Create and return an instance of API client"""
        return SwxApiClient(
            configuration=self.configuration,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            defer_auth=defer_auth
        )

    def get_api_instance(self, api_name):
        """Create and return an instance of required API class"""
        api_client_config = self.get_swxclient()
        if api_name == 'collections':
            return collections_api.CollectionsApi(api_client=api_client_config)
        elif api_name == 'models':
            return models_api.ModelsApi(api_client=api_client_config)
        elif api_name == 'things':
            return things_api.ThingsApi(api_client=api_client_config)
        else:
            return None

class PositivePythonApiClientTestClass(unittest.TestCase):
    """Class that tests positive test cases for PythonApiClient"""

    def setUp(self):

        self.clientAPIInstance = ClientAPIInstance()
        # Set up an instance of the collections API class
        self.collection_api = self.clientAPIInstance.get_api_instance('collections')

        # Set up an instancee of the models API class
        self.model_api = self.clientAPIInstance.get_api_instance('models')

        # Set up an instancee of the things API class
        self.things_api = self.clientAPIInstance.get_api_instance('things')

    @pytest.mark.order(4)
    def test_list_spaces_collections(self):
        """Testing list collections request"""
        print("Testing list collections request")

        # Get a list of existing collections for a given space
        space = pytest.space
        try:
            api_response = self.collection_api.list_spaces_collections(space)
            assert(api_response is not None and 'data' in api_response)
        except swx_sdk.ApiException as e:
            print("Exception when calling CollectionsApi->list_spaces_collections: %s\n" % e)

    def remove_test_spaces_collection(self):
        """Delete test collection"""
        # delete test collection if exists
        try:
            api_response = self.collection_api.list_spaces_collections(pytest.space)
            if api_response is not None:
                coll_list = api_response['data']
                for coll in coll_list:
                    if coll['name'] == COLLECTION_NEW:
                        api_response = self.things_api.list_spaces_collections_things(pytest.space, COLLECTION_NEW)
                        try:
                            if api_response is not None and 'data' in api_response:
                                things_list = api_response['data']
                                if things_list is not None:
                                    for thing_data in things_list:
                                        pytest.THING_ID = thing_data.get('uid', None)
                                        self.things_api.delete_spaces_collections_thing(pytest.space, COLLECTION_NEW, pytest.THING_ID)
                        except swx_sdk.ApiValueError as ve:
                            print("ThingsApi->delete_spaces_collections_thing: test things cleanup.  %s\n" % ve)
                        except swx_sdk.ApiAttributeError as ae:
                            print("ThingsApi->delete_spaces_collections_thing: test things cleanup.  %s\n" % ae)
                        except swx_sdk.ApiException as e:
                            print("ThingsApi->delete_spaces_collections_thing: test things cleanup.  %s\n" % e)
                        self.collection_api.delete_spaces_collection(pytest.space, COLLECTION_NEW)
        except swx_sdk.ApiValueError as ve:
            print("CollectionsApi->delete_spaces_collection: test collection cleanup.  %s\n" % ve)
        except swx_sdk.ApiAttributeError as ae:
            print("CollectionsApi->delete_spaces_collection: test collection cleanup.  %s\n" % ae)
        except swx_sdk.ApiException as e:
            print("CollectionsApi->delete_spaces_collection: test collection cleanup.  %s\n" % e)

    @pytest.mark.order(3)
    def test_add_spaces_collection(self):
        """Testing add collection request"""
        print("Testing add collections request")
        # Create a collection
        space = pytest.space
        collection_request = CollectionRequest(
            name=COLLECTION_NEW,
            description="description created"
        )
        # delete test collection if exists
        self.remove_test_spaces_collection()
        try:
            api_response = self.collection_api.add_spaces_collection(space, collection_request)
            assert(api_response is not None and 'name' in api_response)
        except swx_sdk.ApiAttributeError as ae:
            print("CollectionsApi->delete_spaces_collection: test collection cleanup.  %s\n" % ae)
        except swx_sdk.ApiException as e:
            print("Exception when calling CollectionsApi->add_spaces_collection: %s\n" % e)

    @pytest.mark.order(5)
    def test_update_spaces_collection(self):

        print("Testing update collections request")

        # Update a collection
        space = pytest.space
        collection_name = COLLECTION_NEW
        collection_update_request = CollectionUpdateRequest(
            description="description updated"
        )
        try:
            api_response = self.collection_api.update_spaces_collection(
                space,
                collection_name,
                collection_update_request
            )
            assert(api_response is not None and 'name' in api_response)
        except swx_sdk.ApiException as e:
            print("Exception when calling CollectionsApi->update_spaces_collection: %s\n" % e)

    @pytest.mark.order(26)
    def test_delete_spaces_collection(self):
        """Testing delete collection request"""
        print("Testing delete collections request")

        # Delete an existing collection
        space = pytest.space
        collection_name = COLLECTION_NEW
        try:
            api_response = self.collection_api.delete_spaces_collection(space, collection_name)
            print("test_delete_spaces_collection. api_response ={}".format(api_response))
            assert(api_response is not None and \
                   'error_things_backend' in api_response and \
                   'http_status_code' in api_response['error_things_backend'] and \
                   api_response['error_things_backend']['http_status_code'] == 204)
        except swx_sdk.ApiException as e:
            print("Exception when calling CollectionsApi->delete_spaces_collection: %s\n" % e)

    @pytest.mark.order(7)
    def test_list_spaces_collections_models(self):
        """Testing list models request"""
        print("Testing list models request")

        # Get a list of all existing models in a given collection
        space = pytest.space
        collection_name = COLLECTION_NEW
        try:
            api_response = self.model_api.list_spaces_collections_models(space, collection_name)
            assert(api_response is not None and 'data' in api_response)
        except swx_sdk.ApiException as e:
            print("Exception when calling CollectionsApi->list_spaces_collections_models: %s\n" % e)

    @pytest.mark.order(6)
    def test_add_spaces_collections_model(self):
        """Testing add model request"""
        print("Testing add model request")

        # Create a model in a given collection and space
        space = pytest.space
        collection_name = COLLECTION_NEW
        model_request = ModelRequest(
            name=MODEL_NAME_NEW,
            description="test model description"
        )
        try:
            api_response = self.model_api.add_spaces_collections_model(space, collection_name, model_request)
            assert(api_response is not None and 'name' in api_response)
        except swx_sdk.ApiException as e:
            print("Exception when calling CollectionsApi->add_spaces_collections_model: %s\n" % e)

    @pytest.mark.order(8)
    def test_update_spaces_collections_model(self):
        """Testing update model request"""
        print("Testing update model request")

        # Update a model in specific space, collection
        space = pytest.space
        collection_name = COLLECTION_NEW
        model_name = MODEL_NAME_NEW
        model_update_request = ModelUpdateRequest(
            description="model description updated"
        )

        try:
            api_response = self.model_api.update_spaces_collections_model(
                space,
                collection_name,
                model_name,
                model_update_request
            )
            assert(api_response is not None and 'name' in api_response)
        except swx_sdk.ApiException as e:
            print("Exception when calling CollectionsApi->update_spaces_collections_model: %s\n" % e)

    @pytest.mark.order(24)
    def test_delete_spaces_collections_model(self):
        """Testing delete model request"""
        print("Testing delete model request")

        # Delete a model from a given collection and space
        space = pytest.space
        collection_name = COLLECTION_NEW
        model_name = MODEL_NAME_NEW
        try:
            api_response = self.model_api.delete_spaces_collections_model(space, collection_name, model_name)
            assert(api_response is not None and \
                   'error_things_backend' in api_response and \
                   'http_status_code' in api_response['error_things_backend'] and \
                   api_response['error_things_backend']['http_status_code'] == 204)
        except swx_sdk.ApiException as e:
            print("Exception when calling CollectionsApi->delete_spaces_collections_model: %s\n" % e)

    @pytest.mark.order(11)
    def test_list_spaces_collections_things(self):
        """Testing list things request"""
        print("Testing list things request")

        # Get a list of all existing things in a given collection
        space = pytest.space
        collection_name = COLLECTION_NEW
        try:
            api_response = self.things_api.list_spaces_collections_things(space, collection_name)
            assert(api_response is not None and 'data' in api_response)
        except swx_sdk.ApiValueError as ve:
            print("Exception when calling ThingsApi->list_spaces_collections_things: %s\n" % ve)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError when calling ThingsApi->list_spaces_collections_things: %s\n" % ae)
        except swx_sdk.ApiException as e:
            print("Exception when calling ThingsApi->list_spaces_collections_things: %s\n" % e)

    @pytest.mark.order(10)
    def test_show_spaces_collections_thing(self):
        """Testing show thing request"""
        print("Testing show thing request")

        # Show a thing given collection name, space, thing_id
        space = pytest.space
        collection_name = COLLECTION_NEW
        thing_id = pytest.THING_ID
        try:
            api_response = self.things_api.show_spaces_collections_thing(
                space,
                collection_name,
                thing_id
            )
            assert(api_response is not None and 'uid' in api_response)
        except swx_sdk.ApiValueError as ve:
            print("ApiValueError when calling ThingsApi->show_spaces_collections_thing: %s\n" % ve)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError when calling ThingsApi->show_spaces_collections_thing: %s\n" % ae)
        except swx_sdk.ApiException as e:
            print("Exception when calling ThingsApi->show_spaces_collections_thing: %s\n" % e)

    @pytest.mark.order(9)
    def test_add_spaces_collections_thing(self):
        """Testing add thing request"""
        print("Testing add thing request")
        # Create a thing in a given collection and space
        space = pytest.space
        collection_name = COLLECTION_NEW
        thing_request = ThingRequest(
            title=THING_TITLE_NEW,
            description='thing descr'
        )
        try:
            api_response = self.things_api.add_spaces_collections_thing(space, collection_name, thing_request)
            pytest.THING_ID = api_response['uid']
            assert(api_response is not None and 'uid' in api_response)
        except swx_sdk.ApiException as e:
            print("Exception when calling ThingsApi->add_spaces_collections_thing: %s\n" % e)

    @pytest.mark.order(12)
    def test_update_spaces_collections_thing(self):
        """Testing update thing request"""
        print("Testing update thing request")

        # Update a thing of a given collection and space
        space = pytest.space
        collection_name = COLLECTION_NEW
        thing_id = pytest.THING_ID
        thing_update_request = ThingUpdateRequest(
            description="updated descr"
        )
        try:
            api_response = self.things_api.update_spaces_collections_thing(
                space,
                collection_name,
                thing_id,
                thing_update_request
            )
            assert(api_response is not None and 'uid' in api_response)
        except swx_sdk.ApiValueError as ve:
            print("ApiValueError when calling ThingsApi->update_spaces_collections_thing: %s\n" % ve)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError when calling ThingsApi->update_spaces_collections_thing: %s\n" % ae)
        except swx_sdk.ApiException as e:
            print("Exception when calling ThingsApi->update_spaces_collections_thing: %s\n" % e)

    @pytest.mark.order(25)
    def test_delete_spaces_collections_thing(self):
        """Testing delete thing request"""
        print("Testing delete thing request")

        # Delete a thing from a given collection and space
        space = pytest.space
        collection_name = COLLECTION_NEW
        thing_id = pytest.THING_ID
        try:
            api_response = self.things_api.delete_spaces_collections_thing(space, collection_name, thing_id)
            assert(api_response is not None and \
                   'error_things_backend' in api_response and \
                   'http_status_code' in api_response['error_things_backend'] and \
                   api_response['error_things_backend']['http_status_code'] == 204)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError when calling ThingsApi->delete_spaces_collections_thing: %s\n" % ae)
            assert(True)
        except swx_sdk.ApiException as e:
            print("Exception when calling ThingsApi->delete_spaces_collections_thing: %s\n" % e)

class NegativePythonApiClientTestClass(unittest.TestCase):
    """Class that tests negative test cases for PythonApiClient"""

    def setUp(self):

        self.clientAPIInstance = ClientAPIInstance()
        # Set up an instance of the collections API class
        self.collection_api = self.clientAPIInstance.get_api_instance('collections')

        # Set up an instancee of the models API class
        self.model_api = self.clientAPIInstance.get_api_instance('models')

        # Set up an instancee of the things API class
        self.things_api = self.clientAPIInstance.get_api_instance('things')

    @pytest.mark.order(13)
    def test_list_spaces_collections_space_not_found(self):
        """Testing list collections request"""
        print("Testing list collections request. Space not found")

        # Get a list of existing collections for a given space
        space = "notfound1"
        try:
            api_response = self.collection_api.list_spaces_collections(space)
            assert(api_response is not None)
        except swx_sdk.ApiValueError as ve:
            print("ApiValueError when calling CollectionsApi->list_spaces_collections: %s\n" % ve)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError when calling CollectionsApi->list_spaces_collections:  unsupported attribute error: %s\n" % ae)
            assert(True)
        except swx_sdk.ApiException as e:
            print("Exception when calling CollectionsApi->list_spaces_collections: %s\n" % e)

    @pytest.mark.order(14)
    def test_add_spaces_collection_already_exists(self):
        """Testing add collection request"""
        print("Testing add collections request. Collection already exists.")

        # Create a collection
        space = pytest.space
        collection_name = COLLECTION_NEW
        collection_request = CollectionRequest(
            name=collection_name,
            description='descr1'
        )

        try:
            api_response = self.collection_api.add_spaces_collection(space, collection_request)
            assert(api_response is not None)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError:  unsupported attribute error: %s\n" % ae)
            assert(True)
        except swx_sdk.ApiException as e:
            print("Exception when calling CollectionsApi->test_add_spaces_collection_already_exists: %s\n" % e)

    @pytest.mark.order(15)
    def test_update_spaces_collection_not_found(self):
        """Testing update collection request"""
        print("Testing update collections request. Collection not found.")

        # Update a collection
        space = pytest.space
        collection_name = "notfound1"
        collection_update_request = CollectionUpdateRequest(
            description='descr1'
        )
        try:
            api_response = self.collection_api.update_spaces_collection(
                space,
                collection_name,
                collection_update_request
            )
            assert(api_response is not None)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError:  unsupported attribute error: %s\n" % ae)
            assert(True)
        except swx_sdk.ApiException as e:
            print("Exception when calling CollectionsApi->update_spaces_collection: %s\n" % e)

    @pytest.mark.order(23)
    def test_delete_spaces_collection_not_found(self):
        """Testing delete collection request"""
        print("Testing delete collections request. Collection not found.")

        # Delete an existing collection
        space = pytest.space
        collection_name = 'notfound1'
        try:
            api_response = self.collection_api.delete_spaces_collection(space, collection_name)
            print("test_delete_spaces_collection_not_found. api_response ={}".format(api_response))
            assert(api_response is not None and \
                   'error_things_backend' in api_response and \
                   'http_status_code' in api_response['error_things_backend'] and \
                   api_response['error_things_backend']['http_status_code'] == 204)
        except swx_sdk.ApiException as e:
            print("Exception when calling CollectionsApi->test_delete_spaces_collection_not_found: %s\n" % e)

    @pytest.mark.order(16)
    def test_list_spaces_collections_models_collection_not_found(self):
        """Testing list models request"""
        print("Testing list models request. Collection not found")

        # Get a list of all existing models in a given collection
        space = pytest.space
        collection_name = 'notfound1'
        try:
            api_response = self.model_api.list_spaces_collections_models(space, collection_name)
            assert(api_response is not None)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError:  unsupported attribute error: %s\n" % ae)
            assert(True)
        except swx_sdk.ApiException as e:
            print("Exception when calling ModelsApi->test_list_spaces_collections_models_collection_not_found: %s\n" % e)

    @pytest.mark.order(17)
    def test_add_spaces_collections_model_already_exists(self):
        """Testing add model request"""
        print("Testing add model request. Model already exists.")

        # Create a model in a given collection and space
        space = pytest.space
        collection_name = 'notfound1'
        model_request = ModelRequest(
            name=MODEL_NAME_NEW,
            description="model description"
        )
        try:
            api_response = self.model_api.add_spaces_collections_model(space, collection_name, model_request)
            assert(api_response is not None)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError: unsupported attribute error: %s\n" % ae)
            assert(True)
        except swx_sdk.ApiException as e:
            print("Exception when calling ModelsApi->add_spaces_collections_model: %s\n" % e)

    @pytest.mark.order(18)
    def test_update_spaces_collections_model_not_found(self):
        """Testing update model request"""
        print("Testing update model request. Model not found.")
        # Update a model in specific space, collection
        space = pytest.space
        collection_name = COLLECTION_NEW
        model_name = 'notfound1'
        model_update_request = ModelUpdateRequest(
            description="model description update"
        )
        try:
            api_response = self.model_api.update_spaces_collections_model(
                space,
                collection_name,
                model_name,
                model_update_request
            )
            assert(api_response is not None)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError when calling ModelsApi->update_spaces_collections_model:  unsupported attribute error: %s\n" % ae)
            assert(True)
        except swx_sdk.ApiException as e:
            print("Exception when calling ModelsApi->update_spaces_collections_model: %s\n" % e)

    @pytest.mark.order(19)
    def test_delete_spaces_collections_model_not_found(self):
        """Testing delete model request."""
        print("Testing delete model request. Model not found.")
        # Delete a model from a given collection and space
        space = pytest.space
        collection_name = COLLECTION_NEW
        model_name = "notfound1"
        try:
            api_response = self.model_api.delete_spaces_collections_model(space, collection_name, model_name)
            print("test_delete_spaces_collections_model_not_found. api_response ={}".format(api_response))
            assert(api_response is not None and \
                   'error_things_backend' in api_response and \
                   'http_status_code' in api_response['error_things_backend'] and \
                   api_response['error_things_backend']['http_status_code'] == 204)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError when calling ModelsApi->delete_spaces_collections_model:  unsupported attribute error: %s\n" % ae)
            assert(True)
        except swx_sdk.ApiException as e:
            print("Exception when calling ModelsApi->delete_spaces_collections_model: %s\n" % e)

    @pytest.mark.order(20)
    def test_list_spaces_collections_things_collection_not_found(self):
        """Testing list things request."""
        print("Testing list things request. Collection not found.")

        # Get a list of all existing things in a given collection
        space = pytest.space
        collection_name = 'notfound1'
        try:
            api_response = self.things_api.list_spaces_collections_things(space, collection_name)
            assert(api_response is not None and
                   ('error_things_backend' in api_response or 'data' in api_response and
                    len(api_response['data']) == 0))
        except swx_sdk.ApiValueError as ve:
            print("ApiValueError when calling CollectionsApi->list_spaces_collections: %s\n" % ve)
        except swx_sdk.ApiException as e:
            print("Exception when calling ThingsApi->list_spaces_collections_things: %s\n" % e)

    @pytest.mark.order(21)
    def test_add_spaces_collections_thing_collection_not_found(self):
        """Testing add thing request"""
        print("Testing add thing request. Collection not found.")

        # Create a thing in a given collection and space
        space = pytest.space
        collection_name = 'notfound1'
        thing_request = ThingRequest(
            title=THING_TITLE_NEW,
            description='thing descr'
        )
        try:
            api_response = self.things_api.add_spaces_collections_thing(space, collection_name, thing_request)
            assert(api_response is None)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError: unsupported attribute error: %s\n" % ae)
            assert(True)
        except swx_sdk.ApiException as e:
            print("Exception when calling ThingsApi->add_spaces_collections_thing: %s\n" % e)

    @pytest.mark.order(22)
    def test_update_spaces_collections_thing_not_found(self):
        """Testing update thing request"""
        print("Testing update thing request. Thing id not found.")

        # Update a thing of a given collection and space
        space = pytest.space
        collection_name = COLLECTION_NEW
        thing_id = 'notfound1'
        thing_update_request = ThingUpdateRequest(
            description="updated descr"
        )
        try:
            api_response = self.things_api.update_spaces_collections_thing(
                space,
                collection_name,
                thing_id,
                thing_update_request
            )
            assert(api_response is not None)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError when calling ThingsApi->update_spaces_collections_thing:  unsupported attribute error: %s\n" % ae)
            assert(True)
        except swx_sdk.ApiException as e:
            print("Exception when calling ThingsApi->update_spaces_collections_thing: %s\n" % e)

    @pytest.mark.order(23)
    def test_delete_spaces_collections_thing_not_found(self):
        """Testing delete thing request"""
        print("Testing delete thing request. Thing id not found")

        # Delete a thing from a given collection and space
        space = pytest.space
        collection_name = COLLECTION_NEW
        thing_id = 'notfound1'
        try:
            api_response = self.things_api.delete_spaces_collections_thing(space, collection_name, thing_id)
            assert(api_response is not None and \
                   'error_things_backend' in api_response and \
                   'http_status_code' in api_response['error_things_backend'] and \
                   api_response['error_things_backend']['http_status_code'] == 204)
        except swx_sdk.ApiValueError as ve:
            print("Exception when calling ThingsApi->delete_spaces_collections_thing: %s\n" % ve)
        except swx_sdk.exceptions.ApiAttributeError as ae:
            print("ApiAttributeError when calling ThingsApi->delete_spaces_collections_thing:  unsupported attribute error: %s\n" % ae)
            assert(True)
        except swx_sdk.ApiException as e:
            print("Exception when calling ThingsApi->delete_spaces_collections_thing: %s\n" % e)
