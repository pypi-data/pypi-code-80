# coding: utf-8

"""
    Pure1 Public REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re

# python 2 and python 3 compatibility library
import six
from typing import List, Optional

from .. import models

class FileSystemSnapshotsApi(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def api11_file_system_snapshots_get_with_http_info(
        self,
        authorization=None,  # type: str
        x_request_id=None,  # type: str
        continuation_token=None,  # type: str
        filter=None,  # type: str
        ids=None,  # type: List[str]
        limit=None,  # type: int
        names=None,  # type: List[str]
        offset=None,  # type: int
        sort=None,  # type: List[str]
        source_ids=None,  # type: List[str]
        source_names=None,  # type: List[str]
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.FileSystemSnapshotGetResponse
        """Get FlashBlade file system snapshots

        Retrieves snapshots of FlashBlade file systems. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api11_file_system_snapshots_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param str authorization: Access token (in JWT format) required to use any API endpoint (except `/oauth2`)
        :param str x_request_id: Supplied by client during request or generated by server.
        :param str continuation_token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result. Single quotes are required around all strings.
        :param str filter: Exclude resources that don't match the specified criteria. Single quotes are required around all strings inside the filters.
        :param list[str] ids: A comma-separated list of resource IDs. If there is not at least one resource that matches each `id` element, an error is returned. Single quotes are required around all strings.
        :param int limit: Limit the size of the response to the specified number of resources. A limit of 0 can be used to get the number of resources without getting all of the resources. It will be returned in the total_item_count field. If a client asks for a page size larger than the maximum number, the request is still valid. In that case the server just returns the maximum number of items, disregarding the client's page size request. If not specified, defaults to 1000.
        :param list[str] names: A comma-separated list of resource names. If there is not at least one resource that matches each `name` element, an error is returned. Single quotes are required around all strings.
        :param int offset: The offset of the first resource to return from a collection.
        :param list[str] sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name). If you provide a sort you will not get a continuation token in the response.
        :param list[str] source_ids: A comma-separated list of ids for the source of the object. If there is not at least one resource that matches each `source_id` element, an error is returned. Single quotes are required around all strings.
        :param list[str] source_names: A comma-separated list of names for the source of the object. If there is not at least one resource that matches each `source_name` element, an error is returned. Single quotes are required around all strings.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: FileSystemSnapshotGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        continuation_token = models.quoteString(continuation_token)
        if ids is not None:
            if not isinstance(ids, list):
                ids = [ids]
        ids = models.quoteStrings(ids)
        if names is not None:
            if not isinstance(names, list):
                names = [names]
        names = models.quoteStrings(names)
        if sort is not None:
            if not isinstance(sort, list):
                sort = [sort]
        if source_ids is not None:
            if not isinstance(source_ids, list):
                source_ids = [source_ids]
        source_ids = models.quoteStrings(source_ids)
        if source_names is not None:
            if not isinstance(source_names, list):
                source_names = [source_names]
        source_names = models.quoteStrings(source_names)
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]

        if 'offset' in params and params['offset'] < 0:
            raise ValueError("Invalid value for parameter `offset` when calling `api11_file_system_snapshots_get`, must be a value greater than or equal to `0`")
        collection_formats = {}
        path_params = {}

        query_params = []
        if 'continuation_token' in params:
            query_params.append(('continuation_token', params['continuation_token']))
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
        if 'offset' in params:
            query_params.append(('offset', params['offset']))
        if 'sort' in params:
            query_params.append(('sort', params['sort']))
            collection_formats['sort'] = 'csv'
        if 'source_ids' in params:
            query_params.append(('source_ids', params['source_ids']))
            collection_formats['source_ids'] = 'csv'
        if 'source_names' in params:
            query_params.append(('source_names', params['source_names']))
            collection_formats['source_names'] = 'csv'

        header_params = {}
        if 'authorization' in params:
            header_params['Authorization'] = params['authorization']
        if 'x_request_id' in params:
            header_params['X-Request-ID'] = params['x_request_id']

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(
            ['application/json'])

        # Authentication setting
        auth_settings = ['AuthorizationHeader']

        return self.api_client.call_api(
            '/api/1.1/file-system-snapshots', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FileSystemSnapshotGetResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )

    def api11_file_system_snapshots_policies_get_with_http_info(
        self,
        authorization=None,  # type: str
        x_request_id=None,  # type: str
        continuation_token=None,  # type: str
        filter=None,  # type: str
        limit=None,  # type: int
        member_ids=None,  # type: List[str]
        member_names=None,  # type: List[str]
        policy_ids=None,  # type: List[str]
        policy_names=None,  # type: List[str]
        offset=None,  # type: int
        sort=None,  # type: List[str]
        async_req=False,  # type: bool
        _return_http_data_only=False,  # type: bool
        _preload_content=True,  # type: bool
        _request_timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> models.PolicyMembersGetResponse
        """Get FlashBlade file system snapshot / policy pairs

        Retrieves pairs of FlashBlade file system snapshot members and their policies. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api11_file_system_snapshots_policies_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param str authorization: Access token (in JWT format) required to use any API endpoint (except `/oauth2`)
        :param str x_request_id: Supplied by client during request or generated by server.
        :param str continuation_token: An opaque token used to iterate over a collection. The token to use on the next request is returned in the `continuation_token` field of the result. Single quotes are required around all strings.
        :param str filter: Exclude resources that don't match the specified criteria. Single quotes are required around all strings inside the filters.
        :param int limit: Limit the size of the response to the specified number of resources. A limit of 0 can be used to get the number of resources without getting all of the resources. It will be returned in the total_item_count field. If a client asks for a page size larger than the maximum number, the request is still valid. In that case the server just returns the maximum number of items, disregarding the client's page size request. If not specified, defaults to 1000.
        :param list[str] member_ids: A comma-separated list of member IDs. If there is not at least one resource that matches each `member_id` element, an error is returned. Single quotes are required around all strings.
        :param list[str] member_names: A comma-separated list of member names. If there is not at least one resource that matches each `member_name` element, an error is returned. Single quotes are required around all strings.
        :param list[str] policy_ids: A comma-separated list of policy IDs. If there is not at least one resource that matches each `policy_id` element, an error is returned. Single quotes are required around all strings.
        :param list[str] policy_names: A comma-separated list of policy names. If there is not at least one resource that matches each `policy_name` element, an error is returned. Single quotes are required around all strings.
        :param int offset: The offset of the first resource to return from a collection.
        :param list[str] sort: Sort the response by the specified fields (in descending order if '-' is appended to the field name). If you provide a sort you will not get a continuation token in the response.
        :param bool async_req: Request runs in separate thread and method returns multiprocessing.pool.ApplyResult.
        :param bool _return_http_data_only: Returns only data field.
        :param bool _preload_content: Response is converted into objects.
        :param int _request_timeout: Total request timeout in seconds.
                 It can also be a tuple of (connection time, read time) timeouts.
        :return: PolicyMembersGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        continuation_token = models.quoteString(continuation_token)
        if member_ids is not None:
            if not isinstance(member_ids, list):
                member_ids = [member_ids]
        member_ids = models.quoteStrings(member_ids)
        if member_names is not None:
            if not isinstance(member_names, list):
                member_names = [member_names]
        member_names = models.quoteStrings(member_names)
        if policy_ids is not None:
            if not isinstance(policy_ids, list):
                policy_ids = [policy_ids]
        policy_ids = models.quoteStrings(policy_ids)
        if policy_names is not None:
            if not isinstance(policy_names, list):
                policy_names = [policy_names]
        policy_names = models.quoteStrings(policy_names)
        if sort is not None:
            if not isinstance(sort, list):
                sort = [sort]
        params = {k: v for k, v in six.iteritems(locals()) if v is not None}

        # Convert the filter into a string
        if params.get('filter'):
            params['filter'] = str(params['filter'])
        if params.get('sort'):
            params['sort'] = [str(_x) for _x in params['sort']]

        if 'offset' in params and params['offset'] < 0:
            raise ValueError("Invalid value for parameter `offset` when calling `api11_file_system_snapshots_policies_get`, must be a value greater than or equal to `0`")
        collection_formats = {}
        path_params = {}

        query_params = []
        if 'continuation_token' in params:
            query_params.append(('continuation_token', params['continuation_token']))
        if 'filter' in params:
            query_params.append(('filter', params['filter']))
        if 'limit' in params:
            query_params.append(('limit', params['limit']))
        if 'member_ids' in params:
            query_params.append(('member_ids', params['member_ids']))
            collection_formats['member_ids'] = 'csv'
        if 'member_names' in params:
            query_params.append(('member_names', params['member_names']))
            collection_formats['member_names'] = 'csv'
        if 'policy_ids' in params:
            query_params.append(('policy_ids', params['policy_ids']))
            collection_formats['policy_ids'] = 'csv'
        if 'policy_names' in params:
            query_params.append(('policy_names', params['policy_names']))
            collection_formats['policy_names'] = 'csv'
        if 'offset' in params:
            query_params.append(('offset', params['offset']))
        if 'sort' in params:
            query_params.append(('sort', params['sort']))
            collection_formats['sort'] = 'csv'

        header_params = {}
        if 'authorization' in params:
            header_params['Authorization'] = params['authorization']
        if 'x_request_id' in params:
            header_params['X-Request-ID'] = params['x_request_id']

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(
            ['application/json'])

        # Authentication setting
        auth_settings = ['AuthorizationHeader']

        return self.api_client.call_api(
            '/api/1.1/file-system-snapshots/policies', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PolicyMembersGetResponse',
            auth_settings=auth_settings,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            collection_formats=collection_formats,
        )
