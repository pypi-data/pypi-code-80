# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.11 Python SDK

    Pure Storage FlashBlade REST 1.11 Python SDK. Compatible with REST API versions 1.0 - 1.11. Developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.11
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


class SmtpApi(object):
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

    def list_smtp(self, **kwargs):
        """
        List smtp
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list_smtp(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: SmtpResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.list_smtp_with_http_info(**kwargs)
        else:
            (data) = self.list_smtp_with_http_info(**kwargs)
            return data

    def list_smtp_with_http_info(self, **kwargs):
        """
        List smtp
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list_smtp_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: SmtpResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_smtp" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['AuthTokenHeader']

        return self.api_client.call_api('/1.11/smtp', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='SmtpResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def update_smtp(self, smtp_settings, **kwargs):
        """
        Update smtp
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_smtp(smtp_settings, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param Smtp smtp_settings: (required)
        :return: SmtpResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.update_smtp_with_http_info(smtp_settings, **kwargs)
        else:
            (data) = self.update_smtp_with_http_info(smtp_settings, **kwargs)
            return data

    def update_smtp_with_http_info(self, smtp_settings, **kwargs):
        """
        Update smtp
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_smtp_with_http_info(smtp_settings, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param Smtp smtp_settings: (required)
        :return: SmtpResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['smtp_settings']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_smtp" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'smtp_settings' is set
        if ('smtp_settings' not in params) or (params['smtp_settings'] is None):
            raise ValueError("Missing the required parameter `smtp_settings` when calling `update_smtp`")


        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'smtp_settings' in params:
            body_params = params['smtp_settings']
        # Authentication setting
        auth_settings = ['AuthTokenHeader']

        return self.api_client.call_api('/1.11/smtp', 'PATCH',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='SmtpResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
