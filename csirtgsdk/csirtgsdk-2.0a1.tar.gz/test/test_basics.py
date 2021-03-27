import pytest
from csirtgsdk import risk, search
import responses
from csirtgsdk.constants import REMOTE

from pprint import pprint


@responses.activate
def test_http_risk():
    data = {'first_at': '', 'risk': 'unlikely'}
    responses.add(responses.GET, REMOTE + '/risk',
                  json=data, status=200,
                  headers={'Content-Length': '2'})

    rv = risk('1.1.1.1')
    assert rv == data


@responses.activate
def test_http_risk():
    data = {'first_at': '', 'risk': 'unlikely'}
    responses.add(responses.GET, REMOTE + '/search',
                  json=data, status=200,
                  headers={'Content-Length': '2'})

    rv = search('1.1.1.1')
    assert rv == data
