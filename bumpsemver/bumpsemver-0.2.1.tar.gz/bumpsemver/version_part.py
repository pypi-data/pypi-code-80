import logging
import re
import string

from bumpsemver.exceptions import (
    MissingValueForSerializationException,
    IncompleteVersionRepresentationException,
)
from bumpsemver.functions import NumericFunction
from bumpsemver.utils import key_value_string

logger = logging.getLogger(__name__)


class NumericVersionPartConfiguration:
    function_cls = NumericFunction

    def __init__(self, *args, **kwds):
        self.function = self.function_cls(*args, **kwds)

    @property
    def first_value(self):
        return str(self.function.first_value)

    def bump(self, value=None):
        return self.function.bump(value)


class VersionPart:
    """
    This class represents part of a version number. It contains a self.config
    object that rules how the part behaves when increased or reset.
    """

    def __init__(self, value, config=None):
        self._value = value

        if config is None:
            config = NumericVersionPartConfiguration()

        self.config = config

    @property
    def value(self):
        return self._value

    def copy(self):
        return VersionPart(self._value)

    def bump(self):
        return VersionPart(self.config.bump(self.value), self.config)

    def __format__(self, format_spec):
        return self.value

    def __repr__(self):
        return "<bumpsemver.VersionPart:{}:{}>".format(
            self.config.__class__.__name__, self.value
        )

    def __eq__(self, other):
        return self.value == other.value

    def null(self):
        return VersionPart(self.config.first_value, self.config)


class Version:
    def __init__(self, values, original=None):
        self.values = dict(values)
        self.original = original

    def __getitem__(self, key):
        return self.values[key]

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def __repr__(self):
        return "<bumpsemver.Version:{}>".format(
            key_value_string(self.values))

    def bump(self, part_name, order):
        bumped = False

        new_values = {}

        for label in order:
            if label not in self.values:
                continue
            if label == part_name:
                new_values[label] = self.values[label].bump()
                bumped = True
            elif bumped:
                new_values[label] = self.values[label].null()
            else:
                new_values[label] = self.values[label].copy()

        new_version = Version(new_values)

        return new_version


def labels_for_format(serialize_format):
    return (
        label for _, label, _, _ in string.Formatter().parse(serialize_format)
        if label
    )


class VersionConfig:
    """
    Holds a complete representation of a version string
    """

    def __init__(self, search, replace, part_configs=None):

        self.parse_regex = re.compile(
            r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)", re.VERBOSE)
        self.serialize_format = "{major}.{minor}.{patch}"

        if not part_configs:
            part_configs = {}

        self.part_configs = part_configs
        self.search = search
        self.replace = replace

    def order(self):
        # currently, order depends on the first given serialization format
        # this seems like a good idea because this should be the most
        # complete format
        return labels_for_format(self.serialize_format)

    def parse(self, version_string):
        if not version_string:
            return None

        regexp_one_line = "".join(
            [line.split("#")[0].strip() for line in
             self.parse_regex.pattern.splitlines()]
        )

        logger.info(
            "Parsing version '%s' using regexp '%s'",
            version_string,
            regexp_one_line,
        )

        match = self.parse_regex.search(version_string)

        _parsed = {}
        if not match:
            logger.warning(
                "Evaluating 'parse' option: '%s' does not"
                " parse current version '%s'",
                self.parse_regex.pattern,
                version_string,
            )
            return None

        for key, value in match.groupdict().items():
            _parsed[key] = VersionPart(value, self.part_configs.get(key))

        v = Version(_parsed, version_string)

        logger.info("Parsed the following values: %s",
                    key_value_string(v.values))

        return v

    def _serialize(self, version, serialize_format, context,
                   raise_if_incomplete=False):
        """
        Attempts to serialize a version with the given serialization format.

        Raises MissingValueForSerializationException if not serializable
        """
        values = context.copy()
        for k in version:
            values[k] = version[k]

        try:
            # test whether all parts required in the format have values
            serialized = serialize_format.format(**values)

        except KeyError as e:
            missing_key = getattr(e, "message", e.args[0])
            raise MissingValueForSerializationException(
                "Did not find key {} in {} when"
                " serializing version number".format(repr(missing_key),
                                                     repr(version)
                                                     )
            )

        keys_needing_representation = set()

        for k in self.order():
            v = values[k]

            if not isinstance(v, VersionPart):
                # values coming from environment variables don't need
                # representation
                continue

            keys_needing_representation.add(k)

        required_by_format = set(labels_for_format(serialize_format))

        # try whether all parsed keys are represented
        if raise_if_incomplete:
            if not keys_needing_representation <= required_by_format:
                raise IncompleteVersionRepresentationException(
                    "Could not represent '{}' in format '{}'".format(
                        "', '".join(
                            keys_needing_representation ^ required_by_format),
                        serialize_format,
                    )
                )

        return serialized

    def serialize(self, version, context):
        serialized = self._serialize(version, self.serialize_format, context)
        logger.debug("Serialized to '%s'", serialized)
        return serialized
