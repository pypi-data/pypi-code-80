# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.6 Python SDK

    Pure Storage FlashBlade REST 1.6 Python SDK, developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.6
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class UsageGroupsApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def list_group_usage(self, **kwargs):
        """
        A list of usage group entries
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list_group_usage(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :param str filter: The filter to be used for query.
        :param int limit: limit, should be >= 0
        :param str sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name).
        :param int start: The offset of the first resource to return from a collection.
        :param str token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result.
        :param list[str] file_system_names: A comma-separated list of file system names. If after filtering, there is not at least one resource that matches each of the elements of names, then an error is returned.
        :param list[str] gids: A comma-separated list of group IDs. If after filtering, there is not at least one resource that matches each of the elements of group IDs, then an error is returned. This cannot be provided together with group_names query parameter.
        :param list[str] group_names: A comma-separated list of group names. If after filtering, there is not at least one resource that matches each of the elements of group names, then an error is returned. This cannot be provided together with gids query parameter.
        :return: QuotasGroupResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.list_group_usage_with_http_info(**kwargs)
        else:
            (data) = self.list_group_usage_with_http_info(**kwargs)
            return data

    def list_group_usage_with_http_info(self, **kwargs):
        """
        A list of usage group entries
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list_group_usage_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :param str filter: The filter to be used for query.
        :param int limit: limit, should be >= 0
        :param str sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name).
        :param int start: The offset of the first resource to return from a collection.
        :param str token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result.
        :param list[str] file_system_names: A comma-separated list of file system names. If after filtering, there is not at least one resource that matches each of the elements of names, then an error is returned.
        :param list[str] gids: A comma-separated list of group IDs. If after filtering, there is not at least one resource that matches each of the elements of group IDs, then an error is returned. This cannot be provided together with group_names query parameter.
        :param list[str] group_names: A comma-separated list of group names. If after filtering, there is not at least one resource that matches each of the elements of group names, then an error is returned. This cannot be provided together with gids query parameter.
        :return: QuotasGroupResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['names', 'filter', 'limit', 'sort', 'start', 'token', 'file_system_names', 'gids', 'group_names']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_group_usage" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        path_params = {}

        query_params = []
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'
        if 'filter' in params:
            query_params.append(('filter', params['filter']))
        if 'limit' in params:
            query_params.append(('limit', params['limit']))
        if 'sort' in params:
            query_params.append(('sort', params['sort']))
        if 'start' in params:
            query_params.append(('start', params['start']))
        if 'token' in params:
            query_params.append(('token', params['token']))
        if 'file_system_names' in params:
            query_params.append(('file_system_names', params['file_system_names']))
            collection_formats['file_system_names'] = 'csv'
        if 'gids' in params:
            query_params.append(('gids', params['gids']))
            collection_formats['gids'] = 'csv'
        if 'group_names' in params:
            query_params.append(('group_names', params['group_names']))
            collection_formats['group_names'] = 'csv'

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = ['AuthTokenHeader']

        return self.api_client.call_api('/1.6/usage/groups', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='QuotasGroupResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
