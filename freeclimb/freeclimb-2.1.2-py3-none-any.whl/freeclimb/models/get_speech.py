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


class GetSpeech(object):
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
        'action_url': 'str',
        'grammar_type': 'int',
        'grammar_file': 'str',
        'grammar_rule': 'bool',
        'play_beep': 'str',
        'prompts': 'list[PerclCommand]',
        'no_input_timeout_ms': 'int',
        'recognition_timeout_ms': 'int',
        'confidence_threshold': 'float',
        'sensitivity_level': 'float',
        'speech_complete_timeout_ms': 'int',
        'speech_incomplete_timeout_ms': 'int',
        'privacy_mode': 'bool'
    }

    attribute_map = {
        'action_url': 'actionUrl',
        'grammar_type': 'grammarType',
        'grammar_file': 'grammarFile',
        'grammar_rule': 'grammarRule',
        'play_beep': 'playBeep',
        'prompts': 'prompts',
        'no_input_timeout_ms': 'noInputTimeoutMs',
        'recognition_timeout_ms': 'recognitionTimeoutMs',
        'confidence_threshold': 'confidenceThreshold',
        'sensitivity_level': 'sensitivityLevel',
        'speech_complete_timeout_ms': 'speechCompleteTimeoutMs',
        'speech_incomplete_timeout_ms': 'speechIncompleteTimeoutMs',
        'privacy_mode': 'privacyMode'
    }

    def __init__(self, action_url=None, grammar_type=None, grammar_file=None, grammar_rule=None, play_beep=None, prompts=None, no_input_timeout_ms=None, recognition_timeout_ms=None, confidence_threshold=None, sensitivity_level=None, speech_complete_timeout_ms=None, speech_incomplete_timeout_ms=None, privacy_mode=None, local_vars_configuration=None):  # noqa: E501
        """GetSpeech - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._action_url = None
        self._grammar_type = None
        self._grammar_file = None
        self._grammar_rule = None
        self._play_beep = None
        self._prompts = None
        self._no_input_timeout_ms = None
        self._recognition_timeout_ms = None
        self._confidence_threshold = None
        self._sensitivity_level = None
        self._speech_complete_timeout_ms = None
        self._speech_incomplete_timeout_ms = None
        self._privacy_mode = None
        self.discriminator = None

        self.action_url = action_url
        if grammar_type is not None:
            self.grammar_type = grammar_type
        self.grammar_file = grammar_file
        if grammar_rule is not None:
            self.grammar_rule = grammar_rule
        if play_beep is not None:
            self.play_beep = play_beep
        if prompts is not None:
            self.prompts = prompts
        if no_input_timeout_ms is not None:
            self.no_input_timeout_ms = no_input_timeout_ms
        if recognition_timeout_ms is not None:
            self.recognition_timeout_ms = recognition_timeout_ms
        if confidence_threshold is not None:
            self.confidence_threshold = confidence_threshold
        if sensitivity_level is not None:
            self.sensitivity_level = sensitivity_level
        if speech_complete_timeout_ms is not None:
            self.speech_complete_timeout_ms = speech_complete_timeout_ms
        if speech_incomplete_timeout_ms is not None:
            self.speech_incomplete_timeout_ms = speech_incomplete_timeout_ms
        if privacy_mode is not None:
            self.privacy_mode = privacy_mode

    @property
    def action_url(self):
        """Gets the action_url of this GetSpeech.  # noqa: E501

        When the caller has finished speaking or the command has timed out, FreeClimb will make a POST request to this URL. A PerCL response is expected to continue handling the call.  # noqa: E501

        :return: The action_url of this GetSpeech.  # noqa: E501
        :rtype: str
        """
        return self._action_url

    @action_url.setter
    def action_url(self, action_url):
        """Sets the action_url of this GetSpeech.

        When the caller has finished speaking or the command has timed out, FreeClimb will make a POST request to this URL. A PerCL response is expected to continue handling the call.  # noqa: E501

        :param action_url: The action_url of this GetSpeech.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and action_url is None:  # noqa: E501
            raise ValueError("Invalid value for `action_url`, must not be `None`")  # noqa: E501

        self._action_url = action_url

    @property
    def grammar_type(self):
        """Gets the grammar_type of this GetSpeech.  # noqa: E501

        The grammar file type to use for speech recognition. A value of 'URL' indicates the grammarFile attribute specifies a URL that points to the grammar file. A value of `BUILTIN` indicates the grammarFile attribute specifies the name of one of the platform built-in grammar files.  # noqa: E501

        :return: The grammar_type of this GetSpeech.  # noqa: E501
        :rtype: int
        """
        return self._grammar_type

    @grammar_type.setter
    def grammar_type(self, grammar_type):
        """Sets the grammar_type of this GetSpeech.

        The grammar file type to use for speech recognition. A value of 'URL' indicates the grammarFile attribute specifies a URL that points to the grammar file. A value of `BUILTIN` indicates the grammarFile attribute specifies the name of one of the platform built-in grammar files.  # noqa: E501

        :param grammar_type: The grammar_type of this GetSpeech.  # noqa: E501
        :type: int
        """

        self._grammar_type = grammar_type

    @property
    def grammar_file(self):
        """Gets the grammar_file of this GetSpeech.  # noqa: E501

        The grammar file to use for speech recognition. If grammarType is set to URL, this attribute is specified as a download URL.  # noqa: E501

        :return: The grammar_file of this GetSpeech.  # noqa: E501
        :rtype: str
        """
        return self._grammar_file

    @grammar_file.setter
    def grammar_file(self, grammar_file):
        """Sets the grammar_file of this GetSpeech.

        The grammar file to use for speech recognition. If grammarType is set to URL, this attribute is specified as a download URL.  # noqa: E501

        :param grammar_file: The grammar_file of this GetSpeech.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and grammar_file is None:  # noqa: E501
            raise ValueError("Invalid value for `grammar_file`, must not be `None`")  # noqa: E501

        self._grammar_file = grammar_file

    @property
    def grammar_rule(self):
        """Gets the grammar_rule of this GetSpeech.  # noqa: E501

        The grammar rule within the specified grammar file to use for speech recognition. This attribute is optional if `grammarType` is `URL` and ignored if `grammarType` is `BUILTIN`.  # noqa: E501

        :return: The grammar_rule of this GetSpeech.  # noqa: E501
        :rtype: bool
        """
        return self._grammar_rule

    @grammar_rule.setter
    def grammar_rule(self, grammar_rule):
        """Sets the grammar_rule of this GetSpeech.

        The grammar rule within the specified grammar file to use for speech recognition. This attribute is optional if `grammarType` is `URL` and ignored if `grammarType` is `BUILTIN`.  # noqa: E501

        :param grammar_rule: The grammar_rule of this GetSpeech.  # noqa: E501
        :type: bool
        """

        self._grammar_rule = grammar_rule

    @property
    def play_beep(self):
        """Gets the play_beep of this GetSpeech.  # noqa: E501

        Indicates whether a beep should be played just before speech recognition is initiated so that the speaker can start to speak.  # noqa: E501

        :return: The play_beep of this GetSpeech.  # noqa: E501
        :rtype: str
        """
        return self._play_beep

    @play_beep.setter
    def play_beep(self, play_beep):
        """Sets the play_beep of this GetSpeech.

        Indicates whether a beep should be played just before speech recognition is initiated so that the speaker can start to speak.  # noqa: E501

        :param play_beep: The play_beep of this GetSpeech.  # noqa: E501
        :type: str
        """

        self._play_beep = play_beep

    @property
    def prompts(self):
        """Gets the prompts of this GetSpeech.  # noqa: E501

        The JSON array of PerCL commands to nest within the `GetSpeech` command. The `Say`, `Play`, and `Pause` commands can be used. The nested actions are executed while FreeClimb is waiting for input from the caller. This allows for playing menu options to the caller and to prompt for the expected input. These commands stop executing when the caller begins to input speech.  # noqa: E501

        :return: The prompts of this GetSpeech.  # noqa: E501
        :rtype: list[PerclCommand]
        """
        return self._prompts

    @prompts.setter
    def prompts(self, prompts):
        """Sets the prompts of this GetSpeech.

        The JSON array of PerCL commands to nest within the `GetSpeech` command. The `Say`, `Play`, and `Pause` commands can be used. The nested actions are executed while FreeClimb is waiting for input from the caller. This allows for playing menu options to the caller and to prompt for the expected input. These commands stop executing when the caller begins to input speech.  # noqa: E501

        :param prompts: The prompts of this GetSpeech.  # noqa: E501
        :type: list[PerclCommand]
        """

        self._prompts = prompts

    @property
    def no_input_timeout_ms(self):
        """Gets the no_input_timeout_ms of this GetSpeech.  # noqa: E501

        When recognition is started and there is no speech detected for `noInputTimeoutMs` milliseconds, the recognizer will terminate the recognition operation.  # noqa: E501

        :return: The no_input_timeout_ms of this GetSpeech.  # noqa: E501
        :rtype: int
        """
        return self._no_input_timeout_ms

    @no_input_timeout_ms.setter
    def no_input_timeout_ms(self, no_input_timeout_ms):
        """Sets the no_input_timeout_ms of this GetSpeech.

        When recognition is started and there is no speech detected for `noInputTimeoutMs` milliseconds, the recognizer will terminate the recognition operation.  # noqa: E501

        :param no_input_timeout_ms: The no_input_timeout_ms of this GetSpeech.  # noqa: E501
        :type: int
        """

        self._no_input_timeout_ms = no_input_timeout_ms

    @property
    def recognition_timeout_ms(self):
        """Gets the recognition_timeout_ms of this GetSpeech.  # noqa: E501

        When playback of prompts ends and there is no match for `recognitionTimeoutMs` milliseconds, the recognizer will terminate the recognition operation.  # noqa: E501

        :return: The recognition_timeout_ms of this GetSpeech.  # noqa: E501
        :rtype: int
        """
        return self._recognition_timeout_ms

    @recognition_timeout_ms.setter
    def recognition_timeout_ms(self, recognition_timeout_ms):
        """Sets the recognition_timeout_ms of this GetSpeech.

        When playback of prompts ends and there is no match for `recognitionTimeoutMs` milliseconds, the recognizer will terminate the recognition operation.  # noqa: E501

        :param recognition_timeout_ms: The recognition_timeout_ms of this GetSpeech.  # noqa: E501
        :type: int
        """

        self._recognition_timeout_ms = recognition_timeout_ms

    @property
    def confidence_threshold(self):
        """Gets the confidence_threshold of this GetSpeech.  # noqa: E501

        When a recognition resource recognizes a spoken phrase, it associates a confidence level with that match. Parameter `confidenceThreshold` specifies what confidence level is considered a successful match. Values are between 0.0 and 1.0.  # noqa: E501

        :return: The confidence_threshold of this GetSpeech.  # noqa: E501
        :rtype: float
        """
        return self._confidence_threshold

    @confidence_threshold.setter
    def confidence_threshold(self, confidence_threshold):
        """Sets the confidence_threshold of this GetSpeech.

        When a recognition resource recognizes a spoken phrase, it associates a confidence level with that match. Parameter `confidenceThreshold` specifies what confidence level is considered a successful match. Values are between 0.0 and 1.0.  # noqa: E501

        :param confidence_threshold: The confidence_threshold of this GetSpeech.  # noqa: E501
        :type: float
        """

        self._confidence_threshold = confidence_threshold

    @property
    def sensitivity_level(self):
        """Gets the sensitivity_level of this GetSpeech.  # noqa: E501

        The speech recognizer supports a variable level of sound sensitivity. The sensitivityLevel attribute allows for filtering out background noise, so it is not mistaken for speech. Values are between 0.0 and 1.0   # noqa: E501

        :return: The sensitivity_level of this GetSpeech.  # noqa: E501
        :rtype: float
        """
        return self._sensitivity_level

    @sensitivity_level.setter
    def sensitivity_level(self, sensitivity_level):
        """Sets the sensitivity_level of this GetSpeech.

        The speech recognizer supports a variable level of sound sensitivity. The sensitivityLevel attribute allows for filtering out background noise, so it is not mistaken for speech. Values are between 0.0 and 1.0   # noqa: E501

        :param sensitivity_level: The sensitivity_level of this GetSpeech.  # noqa: E501
        :type: float
        """

        self._sensitivity_level = sensitivity_level

    @property
    def speech_complete_timeout_ms(self):
        """Gets the speech_complete_timeout_ms of this GetSpeech.  # noqa: E501

        Parameter `speechCompleteTimeoutMs` specifies the length of silence required following user speech before the speech recognizer finalizes a result. This timeout applies when the recognizer currently has a complete match against an active grammar. Reasonable speech complete timeout values are typically in the range of 0.3 seconds to 1.0 seconds.  # noqa: E501

        :return: The speech_complete_timeout_ms of this GetSpeech.  # noqa: E501
        :rtype: int
        """
        return self._speech_complete_timeout_ms

    @speech_complete_timeout_ms.setter
    def speech_complete_timeout_ms(self, speech_complete_timeout_ms):
        """Sets the speech_complete_timeout_ms of this GetSpeech.

        Parameter `speechCompleteTimeoutMs` specifies the length of silence required following user speech before the speech recognizer finalizes a result. This timeout applies when the recognizer currently has a complete match against an active grammar. Reasonable speech complete timeout values are typically in the range of 0.3 seconds to 1.0 seconds.  # noqa: E501

        :param speech_complete_timeout_ms: The speech_complete_timeout_ms of this GetSpeech.  # noqa: E501
        :type: int
        """

        self._speech_complete_timeout_ms = speech_complete_timeout_ms

    @property
    def speech_incomplete_timeout_ms(self):
        """Gets the speech_incomplete_timeout_ms of this GetSpeech.  # noqa: E501

        Parameter `speechIncompleteTimeoutMs` specifies the length of silence following user speech after which a recognizer finalizes a result. This timeout applies when the speech prior to the silence is an incomplete match of all active grammars. Timeout `speechIncompleteTimeoutMs` is usually longer than `speechCompleteTimeoutMs` to allow users to pause mid-utterance.  # noqa: E501

        :return: The speech_incomplete_timeout_ms of this GetSpeech.  # noqa: E501
        :rtype: int
        """
        return self._speech_incomplete_timeout_ms

    @speech_incomplete_timeout_ms.setter
    def speech_incomplete_timeout_ms(self, speech_incomplete_timeout_ms):
        """Sets the speech_incomplete_timeout_ms of this GetSpeech.

        Parameter `speechIncompleteTimeoutMs` specifies the length of silence following user speech after which a recognizer finalizes a result. This timeout applies when the speech prior to the silence is an incomplete match of all active grammars. Timeout `speechIncompleteTimeoutMs` is usually longer than `speechCompleteTimeoutMs` to allow users to pause mid-utterance.  # noqa: E501

        :param speech_incomplete_timeout_ms: The speech_incomplete_timeout_ms of this GetSpeech.  # noqa: E501
        :type: int
        """

        self._speech_incomplete_timeout_ms = speech_incomplete_timeout_ms

    @property
    def privacy_mode(self):
        """Gets the privacy_mode of this GetSpeech.  # noqa: E501

        Parameter privacyMode will not log the `text` as required by PCI compliance.  # noqa: E501

        :return: The privacy_mode of this GetSpeech.  # noqa: E501
        :rtype: bool
        """
        return self._privacy_mode

    @privacy_mode.setter
    def privacy_mode(self, privacy_mode):
        """Sets the privacy_mode of this GetSpeech.

        Parameter privacyMode will not log the `text` as required by PCI compliance.  # noqa: E501

        :param privacy_mode: The privacy_mode of this GetSpeech.  # noqa: E501
        :type: bool
        """

        self._privacy_mode = privacy_mode

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
        if not isinstance(other, GetSpeech):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GetSpeech):
            return True

        return self.to_dict() != other.to_dict()

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
