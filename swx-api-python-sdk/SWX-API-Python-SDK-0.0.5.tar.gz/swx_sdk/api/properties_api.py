"""
    Authentication endpoints - OpenAPI 3.0

    The endpoints for the authentication API.  # noqa: E501

    The version of the OpenAPI document: DRAFT
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from swx_sdk.api_client import ApiClient, Endpoint as _Endpoint
from swx_sdk.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from swx_sdk.model.model_property import ModelProperty
from swx_sdk.model.properties import Properties


class PropertiesApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        def __list_accounts_things_properties(
            self,
            account_id,
            thing_id,
            **kwargs
        ):
            """List properties  # noqa: E501

            List all the properties from one thing in array  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.list_accounts_things_properties(account_id, thing_id, async_req=True)
            >>> result = thread.get()

            Args:
                account_id (str):
                thing_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                Properties
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['account_id'] = \
                account_id
            kwargs['thing_id'] = \
                thing_id
            return self.call_with_http_info(**kwargs)

        self.list_accounts_things_properties = _Endpoint(
            settings={
                'response_type': (Properties,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/accounts/{account-id}/things/{thing-id}/properties',
                'operation_id': 'list_accounts_things_properties',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'account_id',
                    'thing_id',
                ],
                'required': [
                    'account_id',
                    'thing_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'account_id':
                        (str,),
                    'thing_id':
                        (str,),
                },
                'attribute_map': {
                    'account_id': 'account-id',
                    'thing_id': 'thing-id',
                },
                'location_map': {
                    'account_id': 'path',
                    'thing_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__list_accounts_things_properties
        )

        def __list_spaces_collections_things_properties(
            self,
            space,
            collection_name,
            thing_id,
            **kwargs
        ):
            """List properties  # noqa: E501

            List all the properties from one thing in array  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.list_spaces_collections_things_properties(space, collection_name, thing_id, async_req=True)
            >>> result = thread.get()

            Args:
                space (str):
                collection_name (str):
                thing_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                Properties
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['space'] = \
                space
            kwargs['collection_name'] = \
                collection_name
            kwargs['thing_id'] = \
                thing_id
            return self.call_with_http_info(**kwargs)

        self.list_spaces_collections_things_properties = _Endpoint(
            settings={
                'response_type': (Properties,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/spaces/{space}/collections/{collection-name}/things/{thing-id}/properties',
                'operation_id': 'list_spaces_collections_things_properties',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'space',
                    'collection_name',
                    'thing_id',
                ],
                'required': [
                    'space',
                    'collection_name',
                    'thing_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'space':
                        (str,),
                    'collection_name':
                        (str,),
                    'thing_id':
                        (str,),
                },
                'attribute_map': {
                    'space': 'space',
                    'collection_name': 'collection-name',
                    'thing_id': 'thing-id',
                },
                'location_map': {
                    'space': 'path',
                    'collection_name': 'path',
                    'thing_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__list_spaces_collections_things_properties
        )

        def __show_accounts_things_property(
            self,
            account_id,
            thing_id,
            _property,
            **kwargs
        ):
            """Show property  # noqa: E501

            Show a property from one thing  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.show_accounts_things_property(account_id, thing_id, _property, async_req=True)
            >>> result = thread.get()

            Args:
                account_id (str):
                thing_id (str):
                _property (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                ModelProperty
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['account_id'] = \
                account_id
            kwargs['thing_id'] = \
                thing_id
            kwargs['_property'] = \
                _property
            return self.call_with_http_info(**kwargs)

        self.show_accounts_things_property = _Endpoint(
            settings={
                'response_type': (ModelProperty,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/accounts/{account-id}/things/{thing-id}/properties/{property}',
                'operation_id': 'show_accounts_things_property',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'account_id',
                    'thing_id',
                    '_property',
                ],
                'required': [
                    'account_id',
                    'thing_id',
                    '_property',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'account_id':
                        (str,),
                    'thing_id':
                        (str,),
                    '_property':
                        (str,),
                },
                'attribute_map': {
                    'account_id': 'account-id',
                    'thing_id': 'thing-id',
                    '_property': 'property',
                },
                'location_map': {
                    'account_id': 'path',
                    'thing_id': 'path',
                    '_property': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__show_accounts_things_property
        )

        def __show_spaces_collections_things_property(
            self,
            space,
            collection_name,
            thing_id,
            _property,
            **kwargs
        ):
            """Show property  # noqa: E501

            Show a property from one thing  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.show_spaces_collections_things_property(space, collection_name, thing_id, _property, async_req=True)
            >>> result = thread.get()

            Args:
                space (str):
                collection_name (str):
                thing_id (str):
                _property (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                ModelProperty
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['space'] = \
                space
            kwargs['collection_name'] = \
                collection_name
            kwargs['thing_id'] = \
                thing_id
            kwargs['_property'] = \
                _property
            return self.call_with_http_info(**kwargs)

        self.show_spaces_collections_things_property = _Endpoint(
            settings={
                'response_type': (ModelProperty,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/spaces/{space}/collections/{collection-name}/things/{thing-id}/properties/{property}',
                'operation_id': 'show_spaces_collections_things_property',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'space',
                    'collection_name',
                    'thing_id',
                    '_property',
                ],
                'required': [
                    'space',
                    'collection_name',
                    'thing_id',
                    '_property',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'space':
                        (str,),
                    'collection_name':
                        (str,),
                    'thing_id':
                        (str,),
                    '_property':
                        (str,),
                },
                'attribute_map': {
                    'space': 'space',
                    'collection_name': 'collection-name',
                    'thing_id': 'thing-id',
                    '_property': 'property',
                },
                'location_map': {
                    'space': 'path',
                    'collection_name': 'path',
                    'thing_id': 'path',
                    '_property': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__show_spaces_collections_things_property
        )

        def __update_accounts_things_property(
            self,
            account_id,
            thing_id,
            _property,
            model_property,
            **kwargs
        ):
            """Update property  # noqa: E501

            Update the value of a property  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.update_accounts_things_property(account_id, thing_id, _property, model_property, async_req=True)
            >>> result = thread.get()

            Args:
                account_id (str):
                thing_id (str):
                _property (str):
                model_property (ModelProperty): Update an existent thing by Id

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                ModelProperty
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['account_id'] = \
                account_id
            kwargs['thing_id'] = \
                thing_id
            kwargs['_property'] = \
                _property
            kwargs['model_property'] = \
                model_property
            return self.call_with_http_info(**kwargs)

        self.update_accounts_things_property = _Endpoint(
            settings={
                'response_type': (ModelProperty,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/accounts/{account-id}/things/{thing-id}/properties/{property}',
                'operation_id': 'update_accounts_things_property',
                'http_method': 'PUT',
                'servers': None,
            },
            params_map={
                'all': [
                    'account_id',
                    'thing_id',
                    '_property',
                    'model_property',
                ],
                'required': [
                    'account_id',
                    'thing_id',
                    '_property',
                    'model_property',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'account_id':
                        (str,),
                    'thing_id':
                        (str,),
                    '_property':
                        (str,),
                    'model_property':
                        (ModelProperty,),
                },
                'attribute_map': {
                    'account_id': 'account-id',
                    'thing_id': 'thing-id',
                    '_property': 'property',
                },
                'location_map': {
                    'account_id': 'path',
                    'thing_id': 'path',
                    '_property': 'path',
                    'model_property': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client,
            callable=__update_accounts_things_property
        )

        def __update_spaces_collections_things_property(
            self,
            space,
            collection_name,
            thing_id,
            _property,
            model_property,
            **kwargs
        ):
            """Update property  # noqa: E501

            Update the value of a property  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.update_spaces_collections_things_property(space, collection_name, thing_id, _property, model_property, async_req=True)
            >>> result = thread.get()

            Args:
                space (str):
                collection_name (str):
                thing_id (str):
                _property (str):
                model_property (ModelProperty): Update an existent thing by Id

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                ModelProperty
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['space'] = \
                space
            kwargs['collection_name'] = \
                collection_name
            kwargs['thing_id'] = \
                thing_id
            kwargs['_property'] = \
                _property
            kwargs['model_property'] = \
                model_property
            return self.call_with_http_info(**kwargs)

        self.update_spaces_collections_things_property = _Endpoint(
            settings={
                'response_type': (ModelProperty,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/spaces/{space}/collections/{collection-name}/things/{thing-id}/properties/{property}',
                'operation_id': 'update_spaces_collections_things_property',
                'http_method': 'PUT',
                'servers': None,
            },
            params_map={
                'all': [
                    'space',
                    'collection_name',
                    'thing_id',
                    '_property',
                    'model_property',
                ],
                'required': [
                    'space',
                    'collection_name',
                    'thing_id',
                    '_property',
                    'model_property',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'space':
                        (str,),
                    'collection_name':
                        (str,),
                    'thing_id':
                        (str,),
                    '_property':
                        (str,),
                    'model_property':
                        (ModelProperty,),
                },
                'attribute_map': {
                    'space': 'space',
                    'collection_name': 'collection-name',
                    'thing_id': 'thing-id',
                    '_property': 'property',
                },
                'location_map': {
                    'space': 'path',
                    'collection_name': 'path',
                    'thing_id': 'path',
                    '_property': 'path',
                    'model_property': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client,
            callable=__update_spaces_collections_things_property
        )
