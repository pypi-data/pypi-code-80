# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.12 Python SDK

    Pure Storage FlashBlade REST 1.12 Python SDK. Compatible with REST API versions 1.0 - 1.12. Developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.12
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


class BucketsApi(object):
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

    def create_buckets(self, **kwargs):
        """
        Create new buckets.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.create_buckets(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :param BucketPost bucket: Bucket create parameters.
        :return: BucketResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.create_buckets_with_http_info(**kwargs)
        else:
            (data) = self.create_buckets_with_http_info(**kwargs)
            return data

    def create_buckets_with_http_info(self, **kwargs):
        """
        Create new buckets.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.create_buckets_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :param BucketPost bucket: Bucket create parameters.
        :return: BucketResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['names', 'bucket']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_buckets" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        path_params = {}

        query_params = []
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'bucket' in params:
            body_params = params['bucket']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['AuthTokenHeader']

        return self.api_client.call_api('/1.12/buckets', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='BucketResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def delete_buckets(self, **kwargs):
        """
        Delete buckets.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_buckets(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param list[str] ids: A comma-separated list of resource IDs. This cannot be provided together with the name or names query parameters.
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.delete_buckets_with_http_info(**kwargs)
        else:
            (data) = self.delete_buckets_with_http_info(**kwargs)
            return data

    def delete_buckets_with_http_info(self, **kwargs):
        """
        Delete buckets.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_buckets_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param list[str] ids: A comma-separated list of resource IDs. This cannot be provided together with the name or names query parameters.
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['ids', 'names']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_buckets" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ids' in params:
            query_params.append(('ids', params['ids']))
            collection_formats['ids'] = 'csv'
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['AuthTokenHeader']

        return self.api_client.call_api('/1.12/buckets', 'DELETE',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type=None,
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def list_buckets(self, **kwargs):
        """
        List buckets
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list_buckets(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str filter: The filter to be used for query.
        :param list[str] ids: A comma-separated list of resource IDs. This cannot be provided together with the name or names query parameters.
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :param int limit: limit, should be >= 0
        :param str sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name).
        :param int start: The offset of the first resource to return from a collection.
        :param str token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result.
        :param bool total_only: Return only the total object.
        :return: BucketResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.list_buckets_with_http_info(**kwargs)
        else:
            (data) = self.list_buckets_with_http_info(**kwargs)
            return data

    def list_buckets_with_http_info(self, **kwargs):
        """
        List buckets
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list_buckets_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str filter: The filter to be used for query.
        :param list[str] ids: A comma-separated list of resource IDs. This cannot be provided together with the name or names query parameters.
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :param int limit: limit, should be >= 0
        :param str sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name).
        :param int start: The offset of the first resource to return from a collection.
        :param str token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result.
        :param bool total_only: Return only the total object.
        :return: BucketResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['filter', 'ids', 'names', 'limit', 'sort', 'start', 'token', 'total_only']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_buckets" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        path_params = {}

        query_params = []
        if 'filter' in params:
            query_params.append(('filter', params['filter']))
        if 'ids' in params:
            query_params.append(('ids', params['ids']))
            collection_formats['ids'] = 'csv'
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'
        if 'limit' in params:
            query_params.append(('limit', params['limit']))
        if 'sort' in params:
            query_params.append(('sort', params['sort']))
        if 'start' in params:
            query_params.append(('start', params['start']))
        if 'token' in params:
            query_params.append(('token', params['token']))
        if 'total_only' in params:
            query_params.append(('total_only', params['total_only']))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['AuthTokenHeader']

        return self.api_client.call_api('/1.12/buckets', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='BucketResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def list_buckets_performance(self, **kwargs):
        """
        List instant or historical bucket performance.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list_buckets_performance(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int resolution: sample frequency in milliseconds
        :param int end_time: Time to end sample in milliseconds since epoch.
        :param str filter: The filter to be used for query.
        :param list[str] ids: A comma-separated list of resource IDs. This cannot be provided together with the name or names query parameters.
        :param int limit: limit, should be >= 0
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :param str sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name).
        :param int start_time: Time to start sample in milliseconds since epoch.
        :param int start: The offset of the first resource to return from a collection.
        :param str token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result.
        :param bool total_only: Return only the total object.
        :return: BucketPerformanceResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.list_buckets_performance_with_http_info(**kwargs)
        else:
            (data) = self.list_buckets_performance_with_http_info(**kwargs)
            return data

    def list_buckets_performance_with_http_info(self, **kwargs):
        """
        List instant or historical bucket performance.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list_buckets_performance_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int resolution: sample frequency in milliseconds
        :param int end_time: Time to end sample in milliseconds since epoch.
        :param str filter: The filter to be used for query.
        :param list[str] ids: A comma-separated list of resource IDs. This cannot be provided together with the name or names query parameters.
        :param int limit: limit, should be >= 0
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :param str sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name).
        :param int start_time: Time to start sample in milliseconds since epoch.
        :param int start: The offset of the first resource to return from a collection.
        :param str token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result.
        :param bool total_only: Return only the total object.
        :return: BucketPerformanceResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['resolution', 'end_time', 'filter', 'ids', 'limit', 'names', 'sort', 'start_time', 'start', 'token', 'total_only']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_buckets_performance" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        path_params = {}

        query_params = []
        if 'resolution' in params:
            query_params.append(('resolution', params['resolution']))
        if 'end_time' in params:
            query_params.append(('end_time', params['end_time']))
        if 'filter' in params:
            query_params.append(('filter', params['filter']))
        if 'ids' in params:
            query_params.append(('ids', params['ids']))
            collection_formats['ids'] = 'csv'
        if 'limit' in params:
            query_params.append(('limit', params['limit']))
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'
        if 'sort' in params:
            query_params.append(('sort', params['sort']))
        if 'start_time' in params:
            query_params.append(('start_time', params['start_time']))
        if 'start' in params:
            query_params.append(('start', params['start']))
        if 'token' in params:
            query_params.append(('token', params['token']))
        if 'total_only' in params:
            query_params.append(('total_only', params['total_only']))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['AuthTokenHeader']

        return self.api_client.call_api('/1.12/buckets/performance', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='BucketPerformanceResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def list_buckets_s3_specific_performance(self, **kwargs):
        """
        List instant or historical bucket object store specific performance.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list_buckets_s3_specific_performance(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int resolution: sample frequency in milliseconds
        :param int end_time: Time to end sample in milliseconds since epoch.
        :param str filter: The filter to be used for query.
        :param list[str] ids: A comma-separated list of resource IDs. This cannot be provided together with the name or names query parameters.
        :param int limit: limit, should be >= 0
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :param str sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name).
        :param int start_time: Time to start sample in milliseconds since epoch.
        :param int start: The offset of the first resource to return from a collection.
        :param str token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result.
        :param bool total_only: Return only the total object.
        :return: BucketS3PerformanceResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.list_buckets_s3_specific_performance_with_http_info(**kwargs)
        else:
            (data) = self.list_buckets_s3_specific_performance_with_http_info(**kwargs)
            return data

    def list_buckets_s3_specific_performance_with_http_info(self, **kwargs):
        """
        List instant or historical bucket object store specific performance.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list_buckets_s3_specific_performance_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int resolution: sample frequency in milliseconds
        :param int end_time: Time to end sample in milliseconds since epoch.
        :param str filter: The filter to be used for query.
        :param list[str] ids: A comma-separated list of resource IDs. This cannot be provided together with the name or names query parameters.
        :param int limit: limit, should be >= 0
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :param str sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name).
        :param int start_time: Time to start sample in milliseconds since epoch.
        :param int start: The offset of the first resource to return from a collection.
        :param str token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result.
        :param bool total_only: Return only the total object.
        :return: BucketS3PerformanceResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['resolution', 'end_time', 'filter', 'ids', 'limit', 'names', 'sort', 'start_time', 'start', 'token', 'total_only']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_buckets_s3_specific_performance" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        path_params = {}

        query_params = []
        if 'resolution' in params:
            query_params.append(('resolution', params['resolution']))
        if 'end_time' in params:
            query_params.append(('end_time', params['end_time']))
        if 'filter' in params:
            query_params.append(('filter', params['filter']))
        if 'ids' in params:
            query_params.append(('ids', params['ids']))
            collection_formats['ids'] = 'csv'
        if 'limit' in params:
            query_params.append(('limit', params['limit']))
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'
        if 'sort' in params:
            query_params.append(('sort', params['sort']))
        if 'start_time' in params:
            query_params.append(('start_time', params['start_time']))
        if 'start' in params:
            query_params.append(('start', params['start']))
        if 'token' in params:
            query_params.append(('token', params['token']))
        if 'total_only' in params:
            query_params.append(('total_only', params['total_only']))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['AuthTokenHeader']

        return self.api_client.call_api('/1.12/buckets/s3-specific-performance', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='BucketS3PerformanceResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def update_buckets(self, **kwargs):
        """
        Update buckets.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_buckets(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param list[str] ids: A comma-separated list of resource IDs. This cannot be provided together with the name or names query parameters.
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :param BucketPatch bucket: Bucket update parameters.
        :return: BucketResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.update_buckets_with_http_info(**kwargs)
        else:
            (data) = self.update_buckets_with_http_info(**kwargs)
            return data

    def update_buckets_with_http_info(self, **kwargs):
        """
        Update buckets.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_buckets_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param list[str] ids: A comma-separated list of resource IDs. This cannot be provided together with the name or names query parameters.
        :param list[str] names: A comma-separated list of resource names. This cannot be provided together with the ids query parameters.
        :param BucketPatch bucket: Bucket update parameters.
        :return: BucketResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['ids', 'names', 'bucket']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_buckets" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ids' in params:
            query_params.append(('ids', params['ids']))
            collection_formats['ids'] = 'csv'
        if 'names' in params:
            query_params.append(('names', params['names']))
            collection_formats['names'] = 'csv'

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'bucket' in params:
            body_params = params['bucket']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['AuthTokenHeader']

        return self.api_client.call_api('/1.12/buckets', 'PATCH',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='BucketResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
