VERSION = "2.0.1"
import maltego_stix2.config
import maltego_stix2.entities
import maltego_stix2.util

from stix2 import CustomObject, CustomObservable, properties

try:
    @CustomObject('x-opencti-incident', [
        ('name', properties.StringProperty(required=True)),
        ('description', properties.StringProperty()),
        ('aliases', properties.ListProperty(properties.StringProperty)),
        ('first_seen', properties.TimestampProperty()),
        ('last_seen', properties.TimestampProperty()),
        ('objective', properties.StringProperty()),
    ])
    class OpenCTIIncident(object):
        pass
except:
    # Already defined by OpenCTI
    pass

@CustomObservable('x-opencti-text', [
    ('value', properties.StringProperty(required=True)),
])
class OpenCTIText(object):
    pass

@CustomObservable('x-opencti-cryptocurrency-wallet', [
    ('value', properties.StringProperty(required=True)),
])
class OpenCTICryptocurrencyWallet(object):
    pass

@CustomObservable('x-opencti-cryptographic-key', [
    ('value', properties.StringProperty(required=True)),
])
class OpenCTICryptographicKey(object):
    pass

@CustomObservable('x-opencti-hostname', [
    ('value', properties.StringProperty(required=True)),
    ('resolves_to_refs', properties.ListProperty(properties.ReferenceProperty(valid_types=['ipv4-addr', 'ipv6-addr', 'domain-name'], spec_version='2.1'))),
])
class OpenCTIHostname(object):
    pass

@CustomObservable('x-opencti-user-agent', [
    ('value', properties.StringProperty(required=True)),
])
class OpenCTIUserAgent(object):
    pass