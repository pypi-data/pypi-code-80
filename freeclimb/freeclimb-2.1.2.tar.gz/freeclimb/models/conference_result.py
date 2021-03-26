# coding: utf-8

"""
    FreeClimb API

    FreeClimb is a cloud-based application programming interface (API) that puts the power of the Vail platform in your hands. FreeClimb simplifies the process of creating applications that can use a full range of telephony features without requiring specialized or on-site telephony equipment. Using the FreeClimb REST API to write applications is easy! You have the option to use the language of your choice or hit the API directly. Your application can execute a command by issuing a RESTful request to the FreeClimb API. The base URL to send HTTP requests to the FreeClimb REST API is: /apiserver. FreeClimb authenticates and processes your request.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: support@freeclimb.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from freeclimb.configuration import Configuration


class ConferenceResult(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'uri': 'str',
        'date_created': 'str',
        'date_updated': 'str',
        'revision': 'int',
        'conference_id': 'str',
        'account_id': 'str',
        'alias': 'str',
        'play_beep': 'str',
        'record': 'bool',
        'status': 'str',
        'wait_url': 'str',
        'action_url': 'str',
        'status_callback_url': 'str',
        'subresource_uris': 'object'
    }

    attribute_map = {
        'uri': 'uri',
        'date_created': 'dateCreated',
        'date_updated': 'dateUpdated',
        'revision': 'revision',
        'conference_id': 'conferenceId',
        'account_id': 'accountId',
        'alias': 'alias',
        'play_beep': 'playBeep',
        'record': 'record',
        'status': 'status',
        'wait_url': 'waitUrl',
        'action_url': 'actionUrl',
        'status_callback_url': 'statusCallbackUrl',
        'subresource_uris': 'subresourceUris'
    }

    def __init__(self, uri=None, date_created=None, date_updated=None, revision=None, conference_id=None, account_id=None, alias=None, play_beep=None, record=None, status=None, wait_url=None, action_url=None, status_callback_url=None, subresource_uris=None, local_vars_configuration=None):  # noqa: E501
        """ConferenceResult - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._uri = None
        self._date_created = None
        self._date_updated = None
        self._revision = None
        self._conference_id = None
        self._account_id = None
        self._alias = None
        self._play_beep = None
        self._record = None
        self._status = None
        self._wait_url = None
        self._action_url = None
        self._status_callback_url = None
        self._subresource_uris = None
        self.discriminator = None

        if uri is not None:
            self.uri = uri
        if date_created is not None:
            self.date_created = date_created
        if date_updated is not None:
            self.date_updated = date_updated
        if revision is not None:
            self.revision = revision
        if conference_id is not None:
            self.conference_id = conference_id
        if account_id is not None:
            self.account_id = account_id
        if alias is not None:
            self.alias = alias
        if play_beep is not None:
            self.play_beep = play_beep
        if record is not None:
            self.record = record
        if status is not None:
            self.status = status
        if wait_url is not None:
            self.wait_url = wait_url
        if action_url is not None:
            self.action_url = action_url
        if status_callback_url is not None:
            self.status_callback_url = status_callback_url
        if subresource_uris is not None:
            self.subresource_uris = subresource_uris

    @property
    def uri(self):
        """Gets the uri of this ConferenceResult.  # noqa: E501

        The URI for this resource, relative to /apiserver.  # noqa: E501

        :return: The uri of this ConferenceResult.  # noqa: E501
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this ConferenceResult.

        The URI for this resource, relative to /apiserver.  # noqa: E501

        :param uri: The uri of this ConferenceResult.  # noqa: E501
        :type: str
        """

        self._uri = uri

    @property
    def date_created(self):
        """Gets the date_created of this ConferenceResult.  # noqa: E501

        The date that this resource was created (GMT) in RFC 1123 format (e.g., Mon, 15 Jun 2009 20:45:30 GMT).  # noqa: E501

        :return: The date_created of this ConferenceResult.  # noqa: E501
        :rtype: str
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """Sets the date_created of this ConferenceResult.

        The date that this resource was created (GMT) in RFC 1123 format (e.g., Mon, 15 Jun 2009 20:45:30 GMT).  # noqa: E501

        :param date_created: The date_created of this ConferenceResult.  # noqa: E501
        :type: str
        """

        self._date_created = date_created

    @property
    def date_updated(self):
        """Gets the date_updated of this ConferenceResult.  # noqa: E501

        The date that this resource was last updated (GMT) in RFC 1123 format (e.g., Mon, 15 Jun 2009 20:45:30 GMT).  # noqa: E501

        :return: The date_updated of this ConferenceResult.  # noqa: E501
        :rtype: str
        """
        return self._date_updated

    @date_updated.setter
    def date_updated(self, date_updated):
        """Sets the date_updated of this ConferenceResult.

        The date that this resource was last updated (GMT) in RFC 1123 format (e.g., Mon, 15 Jun 2009 20:45:30 GMT).  # noqa: E501

        :param date_updated: The date_updated of this ConferenceResult.  # noqa: E501
        :type: str
        """

        self._date_updated = date_updated

    @property
    def revision(self):
        """Gets the revision of this ConferenceResult.  # noqa: E501

        Revision count for the resource. This count is set to 1 on creation and is incremented every time it is updated.  # noqa: E501

        :return: The revision of this ConferenceResult.  # noqa: E501
        :rtype: int
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """Sets the revision of this ConferenceResult.

        Revision count for the resource. This count is set to 1 on creation and is incremented every time it is updated.  # noqa: E501

        :param revision: The revision of this ConferenceResult.  # noqa: E501
        :type: int
        """

        self._revision = revision

    @property
    def conference_id(self):
        """Gets the conference_id of this ConferenceResult.  # noqa: E501

        A string that uniquely identifies this Conference resource.  # noqa: E501

        :return: The conference_id of this ConferenceResult.  # noqa: E501
        :rtype: str
        """
        return self._conference_id

    @conference_id.setter
    def conference_id(self, conference_id):
        """Sets the conference_id of this ConferenceResult.

        A string that uniquely identifies this Conference resource.  # noqa: E501

        :param conference_id: The conference_id of this ConferenceResult.  # noqa: E501
        :type: str
        """

        self._conference_id = conference_id

    @property
    def account_id(self):
        """Gets the account_id of this ConferenceResult.  # noqa: E501

        ID of the account that created this Conference.  # noqa: E501

        :return: The account_id of this ConferenceResult.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this ConferenceResult.

        ID of the account that created this Conference.  # noqa: E501

        :param account_id: The account_id of this ConferenceResult.  # noqa: E501
        :type: str
        """

        self._account_id = account_id

    @property
    def alias(self):
        """Gets the alias of this ConferenceResult.  # noqa: E501

        A description for this Conference.  # noqa: E501

        :return: The alias of this ConferenceResult.  # noqa: E501
        :rtype: str
        """
        return self._alias

    @alias.setter
    def alias(self, alias):
        """Sets the alias of this ConferenceResult.

        A description for this Conference.  # noqa: E501

        :param alias: The alias of this ConferenceResult.  # noqa: E501
        :type: str
        """

        self._alias = alias

    @property
    def play_beep(self):
        """Gets the play_beep of this ConferenceResult.  # noqa: E501

        Setting that controls when a beep is played. One of: always, never, entryOnly, exitOnly. Defaults to always.  # noqa: E501

        :return: The play_beep of this ConferenceResult.  # noqa: E501
        :rtype: str
        """
        return self._play_beep

    @play_beep.setter
    def play_beep(self, play_beep):
        """Sets the play_beep of this ConferenceResult.

        Setting that controls when a beep is played. One of: always, never, entryOnly, exitOnly. Defaults to always.  # noqa: E501

        :param play_beep: The play_beep of this ConferenceResult.  # noqa: E501
        :type: str
        """
        allowed_values = ["always", "never", "entryOnly", "exitOnly"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and play_beep not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `play_beep` ({0}), must be one of {1}"  # noqa: E501
                .format(play_beep, allowed_values)
            )

        self._play_beep = play_beep

    @property
    def record(self):
        """Gets the record of this ConferenceResult.  # noqa: E501

        Flag indicating whether recording is enabled for this Conference.  # noqa: E501

        :return: The record of this ConferenceResult.  # noqa: E501
        :rtype: bool
        """
        return self._record

    @record.setter
    def record(self, record):
        """Sets the record of this ConferenceResult.

        Flag indicating whether recording is enabled for this Conference.  # noqa: E501

        :param record: The record of this ConferenceResult.  # noqa: E501
        :type: bool
        """

        self._record = record

    @property
    def status(self):
        """Gets the status of this ConferenceResult.  # noqa: E501

        The status of the Conference. One of: creating, empty, populated, inProgress, or terminated.  # noqa: E501

        :return: The status of this ConferenceResult.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ConferenceResult.

        The status of the Conference. One of: creating, empty, populated, inProgress, or terminated.  # noqa: E501

        :param status: The status of this ConferenceResult.  # noqa: E501
        :type: str
        """
        allowed_values = ["creating", "empty", "populated", "inProgress", "terminated"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and status not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def wait_url(self):
        """Gets the wait_url of this ConferenceResult.  # noqa: E501

        URL referencing the audio file to be used as default wait music for the Conference when it is in the populated state.  # noqa: E501

        :return: The wait_url of this ConferenceResult.  # noqa: E501
        :rtype: str
        """
        return self._wait_url

    @wait_url.setter
    def wait_url(self, wait_url):
        """Sets the wait_url of this ConferenceResult.

        URL referencing the audio file to be used as default wait music for the Conference when it is in the populated state.  # noqa: E501

        :param wait_url: The wait_url of this ConferenceResult.  # noqa: E501
        :type: str
        """

        self._wait_url = wait_url

    @property
    def action_url(self):
        """Gets the action_url of this ConferenceResult.  # noqa: E501

        URL invoked once the Conference is successfully created.  # noqa: E501

        :return: The action_url of this ConferenceResult.  # noqa: E501
        :rtype: str
        """
        return self._action_url

    @action_url.setter
    def action_url(self, action_url):
        """Sets the action_url of this ConferenceResult.

        URL invoked once the Conference is successfully created.  # noqa: E501

        :param action_url: The action_url of this ConferenceResult.  # noqa: E501
        :type: str
        """

        self._action_url = action_url

    @property
    def status_callback_url(self):
        """Gets the status_callback_url of this ConferenceResult.  # noqa: E501

        URL to inform that the Conference status has changed.  # noqa: E501

        :return: The status_callback_url of this ConferenceResult.  # noqa: E501
        :rtype: str
        """
        return self._status_callback_url

    @status_callback_url.setter
    def status_callback_url(self, status_callback_url):
        """Sets the status_callback_url of this ConferenceResult.

        URL to inform that the Conference status has changed.  # noqa: E501

        :param status_callback_url: The status_callback_url of this ConferenceResult.  # noqa: E501
        :type: str
        """

        self._status_callback_url = status_callback_url

    @property
    def subresource_uris(self):
        """Gets the subresource_uris of this ConferenceResult.  # noqa: E501

        The list of subresources for this Conference. This includes participants and/or recordings.  # noqa: E501

        :return: The subresource_uris of this ConferenceResult.  # noqa: E501
        :rtype: object
        """
        return self._subresource_uris

    @subresource_uris.setter
    def subresource_uris(self, subresource_uris):
        """Sets the subresource_uris of this ConferenceResult.

        The list of subresources for this Conference. This includes participants and/or recordings.  # noqa: E501

        :param subresource_uris: The subresource_uris of this ConferenceResult.  # noqa: E501
        :type: object
        """

        self._subresource_uris = subresource_uris

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.to_camel_case(attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            elif value is None:
                continue
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ConferenceResult):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ConferenceResult):
            return True

        return self.to_dict() != other.to_dict()

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
