# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/annotations/scope.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='eolymp/annotations/scope.proto',
  package='eolymp.api',
  syntax='proto3',
  serialized_options=b'Z=github.com/eolymp/contracts/go/eolymp/annotations;annotations',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1e\x65olymp/annotations/scope.proto\x12\neolymp.api\x1a google/protobuf/descriptor.proto\"\x18\n\x05Scope\x12\x0f\n\x05scope\x18\xb1\xac\x01 \x03(\t:B\n\x05scope\x12\x1e.google.protobuf.MethodOptions\x18\xb0\xac\x01 \x01(\x0b\x32\x11.eolymp.api.ScopeB?Z=github.com/eolymp/contracts/go/eolymp/annotations;annotationsb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_descriptor__pb2.DESCRIPTOR,])


SCOPE_FIELD_NUMBER = 22064
scope = _descriptor.FieldDescriptor(
  name='scope', full_name='eolymp.api.scope', index=0,
  number=22064, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key)


_SCOPE = _descriptor.Descriptor(
  name='Scope',
  full_name='eolymp.api.Scope',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='scope', full_name='eolymp.api.Scope.scope', index=0,
      number=22065, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=80,
  serialized_end=104,
)

DESCRIPTOR.message_types_by_name['Scope'] = _SCOPE
DESCRIPTOR.extensions_by_name['scope'] = scope
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Scope = _reflection.GeneratedProtocolMessageType('Scope', (_message.Message,), {
  'DESCRIPTOR' : _SCOPE,
  '__module__' : 'eolymp.annotations.scope_pb2'
  # @@protoc_insertion_point(class_scope:eolymp.api.Scope)
  })
_sym_db.RegisterMessage(Scope)

scope.message_type = _SCOPE
google_dot_protobuf_dot_descriptor__pb2.MethodOptions.RegisterExtension(scope)

DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
