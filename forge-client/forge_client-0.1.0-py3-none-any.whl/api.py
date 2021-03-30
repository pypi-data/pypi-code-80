import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass
class Credential:

    client_id: str
    client_secret: str


@dataclass
class AuthToken:

    access_token: str
    token_type: str
    expires_in: int


@dataclass
class _Bucket:

    bucket_key: str
    created_date: int
    policy_key: str

    @classmethod
    def from_response(cls, resp: Dict[str, Any]):
        return cls(
            bucket_key=resp['bucketKey'],
            created_date=resp['createdDate'],
            policy_key=resp['policyKey']
        )


@dataclass
class Bucket:

    bucket_key: str
    created_date: int
    policy_key: str
    bucket_owner: Optional[str] = None
    permissions: Optional[List[Dict[str, str]]] = None

    @classmethod
    def from_response(cls, resp: Dict[str, Any]):
        return cls(
            bucket_key=resp['bucketKey'],
            bucket_owner=resp.get('bucketOwner', None),
            created_date=resp['createdDate'],
            permissions=resp.get('permissions', None),
            policy_key=resp['policyKey']
        )


@dataclass
class Object:

    bucket_key: str
    object_id: str
    object_key: str
    sha1: str
    size: int
    content_type: Optional[str]
    location: str

    @classmethod
    def from_response(cls, resp: Dict[str, Any]):
        return cls(
            bucket_key=resp['bucketKey'],
            object_id=resp['objectId'],
            object_key=resp['objectKey'],
            sha1=resp['sha1'],
            size=resp['size'],
            content_type=resp.get('contentType', None),
            location=resp['location']
        )


def _check_region(region: str) -> None:
    if region not in ('US', 'EMEA'):
        raise ValueError('region must be "US" or "EMEA".')


def _check_policy_key(policy_key: str) -> None:
    if policy_key not in ('transient', 'temporary', 'persistent'):
        raise ValueError('policy_key must be "transient", "temporary" or "persistent".')


class ForgeClient:

    base_url: str = 'https://developer.api.autodesk.com'

    def __init__(self, credential: Credential):
        self.credential: Credential = credential
        self.auth_token: Optional[AuthToken] = self.authemticate(self.credential)

    def authemticate(
        self,
        credential: Credential,
        scope: str = 'data:read data:write bucket:create bucket:read bucket:delete'
    ) -> Optional[AuthToken]:
        url: str = self.base_url + '/authentication/v1/authenticate'
        headers: Dict[str, str] = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body: Dict[str, str] = {
            'client_id': credential.client_id,
            'client_secret': credential.client_secret,
            'grant_type': 'client_credentials',
            'scope': scope
        }
        r = requests.post(url, data=body, headers=headers)
        if r.status_code == 200:
            return AuthToken(**r.json())
        return None

    def list_buckets(
        self, region: str = 'US', limit: int = 10
    ) -> Optional[List[Bucket]]:
        ''' Get a list of buckets in OSS.
            https://forge.autodesk.com/en/docs/data/v2/reference/http/buckets-GET/
        '''
        url: str = self.base_url + '/oss/v2/buckets'
        headers: Dict[str, str] = {
            'Authorization': f'Bearer {self.auth_token.access_token}',
        }
        query_params: Dict[str, Any] = {
            'region': region,
            'limit': limit,
        }
        r = requests.get(url, headers=headers, params=query_params)
        if r.status_code != 200:
            print(r.json())
            return None
        items: List[Bucket] = [
            Bucket.from_response(item) for item in r.json()['items']
        ]
        return items

    def get_bucket(self, bucket_key: str) -> Optional[Bucket]:
        '''https://forge.autodesk.com/en/docs/data/v2/reference/http/buckets-:bucketKey-details-GET/'''
        url: str = self.base_url + f'/oss/v2/buckets/{bucket_key}/details'
        headers: Dict[str, str] = {
            'Authorization': f'Bearer {self.auth_token.access_token}',
        }
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(r.json())
            return None
        return Bucket.from_response(r.json())

    def create_bucket(
        self, bucket_key: str, policy_key: str, region: str = 'US'
    ) -> Optional[Bucket]:
        '''https://forge.autodesk.com/en/docs/data/v2/reference/http/buckets-POST/'''
        _check_region(region)
        _check_policy_key(policy_key)

        url: str = self.base_url + '/oss/v2/buckets'
        headers: Dict[str, str] = {
            'Authorization': f'Bearer {self.auth_token.access_token}',
            'Content-Type': 'application/json',
            'x-ads-region': region
        }
        body: Dict[str, Any] = {
            'bucketKey': bucket_key,
            'policyKey': policy_key
        }
        r = requests.post(url, data=json.dumps(body), headers=headers)
        if r.status_code != 200:
            print(r.json())
            return None
        return Bucket.from_response(r.json())

    def delete_bucket(self, bucket_key: str) -> int:
        url: str = self.base_url + f'/oss/v2/buckets/{bucket_key}'
        headers: Dict[str, str] = {
            'Authorization': f'Bearer {self.auth_token.access_token}',
        }
        r = requests.delete(url, headers=headers)
        return r.status_code

    def upload_object(
        self, object_path: str, bucket_key: str
    ) -> Optional[Object]:
        '''https://forge.autodesk.com/en/docs/data/v2/reference/http/buckets-:bucketKey-objects-:objectName-PUT/'''
        object_name: str = os.path.basename(object_path)
        url: str = self.base_url + f'/oss/v2/buckets/{bucket_key}/objects/{object_name}'
        headers: Dict[str, str] = {
            'Authorization': f'Bearer {self.auth_token.access_token}',
            'Content-Type' : 'application/octet-stream',
        }
        with open(object_path, 'rb') as f:
            r = requests.put(url, headers=headers, data=f)
            if r.status_code != 200:
                print(r.json())
                return None
            return Object.from_response(r.json())

    def list_objects(
        self,
        bucket_key: str,
        limit: Optional[int] = None,
        begins_with: Optional[str] = None,
        start_at: Optional[str] = None
    ) -> Optional[Object]:
        '''https://forge.autodesk.com/en/docs/data/v2/reference/http/buckets-:bucketKey-objects-GET/'''
        url: str = self.base_url + f'/oss/v2/buckets/{bucket_key}/objects'
        headers: Dict[str, str] = {
            'Authorization': f'Bearer {self.auth_token.access_token}',
        }
        query_params: Dict[str, Any] = {
            'limit': limit,
            'beginsWith': begins_with,
            'startAt': start_at
        }
        r = requests.get(url, headers=headers, params=query_params)
        if r.status_code != 200:
            print(r.text)
            return None
        items: List[Object] = [
            Object.from_response(item) for item in r.json()['items']
        ]
        return items

    def get_object(self, bucket_key: str, object_key: str) -> Optional[Object]:
        '''https://forge.autodesk.com/en/docs/data/v2/reference/http/buckets-:bucketKey-objects-:objectName-details-GET/'''
        url: str = self.base_url + f'/oss/v2/buckets/{bucket_key}/objects/{object_key}/details'
        headers: Dict[str, str] = {
            'Authorization': f'Bearer {self.auth_token.access_token}',
        }
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(r.text)
            return None
        return Object.from_response(r.json())

    def translate_format(self, urn: str, format_type: str, region: str):
        _check_region(region)

        url: str = self.base_url + '/modelderivative/v2/designdata/job'
        headers: Dict[str, Any] = {
            'Authorization': f'Bearer {self.auth_token.access_token}',
            'Content-Type': 'application/json',
        }
        body: Dict[str, Any] = {
            'input': {'urn': urn},
            'output': {
                'destination': {'region': region},
                'formats': [{'type': format_type}]
            }
        }
        r = requests.post(url, data=json.dumps(body), headers=headers)
        print(r)
        print(r.text)
        print(r.json())
