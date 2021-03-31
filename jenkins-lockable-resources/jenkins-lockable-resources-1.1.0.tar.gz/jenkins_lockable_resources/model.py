#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

"""
Jenkins Lockable Resources plugin API

This library aims to query Jenkins Lockable Resources plugin to retieve information or control resources.
"""

import re

from bs4 import BeautifulSoup
from jenkinsapi.jenkinsbase import JenkinsBase


PLUGIN_NAME = "lockable-resources"

def data_resource_from_row(row):
    name = str(row.attrs["data-resource-name"])
    columns = row.find_all("td")
    state_cell = columns[1]
    state_cell_text = state_cell.text.strip()
    parts = state_cell_text.split("\n")
    state, *parts = parts
    owner = parts[1].strip() if len(parts) > 1 else None
    label = str(columns[2].text)
    return dict(name=name, state=state, owner=owner, label=label)


def check_request(f):
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        if not response.ok:
            response.raise_for_status()
    return wrapper

class Resource:
    def __init__(
        self, jenkins_obj, name, state, owner, label=None, ephemeral=False, **kwargs
    ):
        self.jenkins = jenkins_obj.get_jenkins_obj()
        self.name = name
        self.state = state
        self.owner = owner
        self.label = label
        self.ephemeral = ephemeral
        self.baseurl = jenkins_obj.baseurl

    def is_locked(self):
        """
        Check if resource is locked
        """
        return self.state == "LOCKED"

    def is_reserved(self):
        """
        Check if resource is reserved
        """
        return self.state == "RESERVED"

    def is_free(self):
        """
        Check if resource is free
        """
        return self.state == "FREE"

    def is_owned(self):
        """
        Check if resource is owned by current user
        """
        return self.owner == self.jenkins.username

    @check_request
    def reserve(self):
        """
        Reserve the resource
        """
        url = f"{self.baseurl}/reserve?resource={self.name}"
        return self.jenkins.requester.post_url(url)

    @check_request
    def unreserve(self):
        """
        Unreserve the resource
        """
        url = f"{self.baseurl}/unreserve?resource={self.name}"
        return self.jenkins.requester.post_url(url)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(
            dict(name=self.name, state=self.state, owner=self.owner, label=self.label)
        )


class LockableResources(JenkinsBase):

    """
    Class to hold information on locakble resources
    """

    def __init__(
        self,
        jenkins_obj,
        baseurl=None,
        poll=True,
        res_filter=None,
    ):
        """
        Init a lockable resource object

        Args:
            jenkins_obj (Jenkins): ref to the jenkins obj
            baseurl (str): basic url for querying information on a node
                If url is not set - object will construct it itself. This is
                useful when node is being created and not exists in Jenkins yet
            poll (bool): set to False if node does not exist or automatic
                refresh from Jenkins is not required. Default is True.
                If baseurl parameter is set to None - poll parameter will be
                set to False
            res_filter (str): Regex expression to filter resources (default '.*')
        """

        self.jenkins = jenkins_obj
        self.plugin = self.get_plugin()
        if not baseurl:
            poll = False
            baseurl = f"{self.jenkins.baseurl}/{PLUGIN_NAME}/"

        self._filter = re.compile(res_filter) if res_filter else re.compile(".*")
        self._cache_data = {}
        self._data = None

        JenkinsBase.__init__(self, baseurl, poll=poll)

    def get_plugin(self):
        # Check plugin availablility and version
        plugins = self.get_jenkins_obj().plugins
        return plugins[PLUGIN_NAME]

    def get_jenkins_obj(self):
        return self.jenkins

    def get_data(self, url, params=None, tree=None):
        """
        Retrieve data of lockable-resources
        """
        requester = self.get_jenkins_obj().requester
        response = requester.post_url(self.baseurl)
        if not response.ok:
            response.raise_for_status()

        # Scrap page for data
        html_soup = BeautifulSoup(response.text, "html.parser")
        main = html_soup.find("div", id="main-panel")
        table = main.find("table", class_="pane")
        rows = table.find_all("tr", attrs={"data-resource-name": self._filter})
        # Iterate through rows to extract resource name state and ownership
        self._cache_data["resources"] = list(map(data_resource_from_row, rows))

        return self._cache_data

    @property
    def data(self):
        if self._data is None:
            self._data = self.poll()
        return self._data.get("resources", [])

    def list_resources(self) -> list:
        """
        Lists resources names
        """
        return list(self.keys())

    def get_resources(self) -> list:
        """
        Get resources
        """
        return list(self.values())

    def is_reserved(self, name) -> bool:
        """
        Check if a resource is reserved

        Args:
            name (str): The resource name
        """
        return self[name].is_reserved()

    def is_free(self, name) -> bool:
        """
        Check if resource is free
        """
        return self[name].is_free()

    def get_owner(self, name) -> str:
        """
        Get resource owner

        Args:
            name (str): The resource name
        """
        return self[name].owner

    def get_owned_resources(self, user=None) -> list:
        """
        Get resources owned by user

        Args:
            user (str): The owner name. Default to the current jenkins user.
        """
        if user is None:
            user = self.jenkins.username

        return [res for res in self.values() if res.is_reserved and res.owner == user]

    def get_free_resources(self) -> list:
        """
        Find a free resource
        """
        return [res for res in self.values() if res.is_free()]

    def reserve(self, name):
        """
        Reserve a resource
        """
        self[name].reserve()

    def unreserve(self, name):
        """
        Unreserve a resource
        """
        self[name].unreserve()

    def items(self):
        """
        Iterate over the names & objects for all resources
        """
        for resource in self.values():
            yield resource.name, resource

    def keys(self):
        """
        Iterate over the names of all available resources
        """
        for row in self.data:
            yield row["name"]

    def values(self, name=None, label=None, state=None):
        """
        Iterate over all available resources

        Args:
            name (str): a regex match string for resource name
            label (str): a regex match string for resource name
            state (str): the state to match (case insensitive)
        """
        data = self.data
        if name is not None:
            if isinstance(name, str):
                name = re.compile(name)
            data = filter(lambda x: name.match(x["name"]), data)
        if label is not None:
            if isinstance(label, str):
                label = re.compile(label)
            data = filter(lambda x: label.match(x["label"]), data)
        if state is not None:
            state = state.upper()
            data = filter(lambda x: x["state"] == state, data)

        for attrs in data:
            yield self._make_resource(attrs)

    def _make_resource(self, attrs):
        return Resource(self, **attrs)

    def __contains__(self, resource):
        """
        True if resource exists in Jenkins
        """
        return resource in self.keys()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        # Regex key search
        pattern = re.compile(key)
        for attrs in self.data:
            if pattern.match(attrs["name"]):
                return self._make_resource(attrs)
        raise KeyError(key)

    def __str__(self):
        return self.baseurl
