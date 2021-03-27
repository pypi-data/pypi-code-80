# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: graph_vector.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='graph_vector.proto',
  package='',
  serialized_pb=_b('\n\x12graph_vector.proto\"\x82\x0b\n\x0bVectorGraph\x12\x0f\n\x07version\x18\x01 \x02(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12$\n\x04type\x18\x03 \x02(\x0e\x32\x16.VectorGraph.GraphType\x12\x13\n\x0bvertexCount\x18\x04 \x02(\r\x12\x11\n\tedgeCount\x18\x05 \x02(\r\x12 \n\x05\x65\x64ges\x18\x06 \x03(\x0b\x32\x11.VectorGraph.Edge\x12:\n\x0euint32_vectors\x18\x07 \x03(\x0b\x32\".VectorGraph.UInt32AttributeVector\x12:\n\x0e\x64ouble_vectors\x18\x08 \x03(\x0b\x32\".VectorGraph.DoubleAttributeVector\x12:\n\x0estring_vectors\x18\t \x03(\x0b\x32\".VectorGraph.StringAttributeVector\x12\x38\n\rint32_vectors\x18\n \x03(\x0b\x32!.VectorGraph.Int32AttributeVector\x12\x38\n\rint64_vectors\x18\x0b \x03(\x0b\x32!.VectorGraph.Int64AttributeVector\x12\x38\n\rfloat_vectors\x18\x0c \x03(\x0b\x32!.VectorGraph.FloatAttributeVector\x12\x36\n\x0c\x62ool_vectors\x18\r \x03(\x0b\x32 .VectorGraph.BoolAttributeVector\x1a \n\x04\x45\x64ge\x12\x0b\n\x03src\x18\x01 \x02(\r\x12\x0b\n\x03\x64st\x18\x02 \x02(\r\x1ag\n\x15UInt32AttributeVector\x12\x0c\n\x04name\x18\x01 \x02(\t\x12,\n\x06target\x18\x02 \x02(\x0e\x32\x1c.VectorGraph.AttributeTarget\x12\x12\n\x06values\x18\x03 \x03(\rB\x02\x10\x01\x1a\x66\n\x14Int32AttributeVector\x12\x0c\n\x04name\x18\x01 \x02(\t\x12,\n\x06target\x18\x02 \x02(\x0e\x32\x1c.VectorGraph.AttributeTarget\x12\x12\n\x06values\x18\x03 \x03(\x05\x42\x02\x10\x01\x1a\x66\n\x14Int64AttributeVector\x12\x0c\n\x04name\x18\x01 \x02(\t\x12,\n\x06target\x18\x02 \x02(\x0e\x32\x1c.VectorGraph.AttributeTarget\x12\x12\n\x06values\x18\x03 \x03(\x03\x42\x02\x10\x01\x1a\x66\n\x14\x46loatAttributeVector\x12\x0c\n\x04name\x18\x01 \x02(\t\x12,\n\x06target\x18\x02 \x02(\x0e\x32\x1c.VectorGraph.AttributeTarget\x12\x12\n\x06values\x18\x03 \x03(\x02\x42\x02\x10\x01\x1ag\n\x15\x44oubleAttributeVector\x12\x0c\n\x04name\x18\x01 \x02(\t\x12,\n\x06target\x18\x02 \x02(\x0e\x32\x1c.VectorGraph.AttributeTarget\x12\x12\n\x06values\x18\x03 \x03(\x01\x42\x02\x10\x01\x1a\x63\n\x15StringAttributeVector\x12\x0c\n\x04name\x18\x01 \x02(\t\x12,\n\x06target\x18\x02 \x02(\x0e\x32\x1c.VectorGraph.AttributeTarget\x12\x0e\n\x06values\x18\x03 \x03(\t\x1a\x65\n\x13\x42oolAttributeVector\x12\x0c\n\x04name\x18\x01 \x02(\t\x12,\n\x06target\x18\x02 \x02(\x0e\x32\x1c.VectorGraph.AttributeTarget\x12\x12\n\x06values\x18\x03 \x03(\x08\x42\x02\x10\x01\")\n\tGraphType\x12\x0e\n\nUNDIRECTED\x10\x00\x12\x0c\n\x08\x44IRECTED\x10\x01\"\'\n\x0f\x41ttributeTarget\x12\n\n\x06VERTEX\x10\x00\x12\x08\n\x04\x45\x44GE\x10\x01')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_VECTORGRAPH_GRAPHTYPE = _descriptor.EnumDescriptor(
  name='GraphType',
  full_name='VectorGraph.GraphType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNDIRECTED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DIRECTED', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1351,
  serialized_end=1392,
)
_sym_db.RegisterEnumDescriptor(_VECTORGRAPH_GRAPHTYPE)

_VECTORGRAPH_ATTRIBUTETARGET = _descriptor.EnumDescriptor(
  name='AttributeTarget',
  full_name='VectorGraph.AttributeTarget',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='VERTEX', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EDGE', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1394,
  serialized_end=1433,
)
_sym_db.RegisterEnumDescriptor(_VECTORGRAPH_ATTRIBUTETARGET)


_VECTORGRAPH_EDGE = _descriptor.Descriptor(
  name='Edge',
  full_name='VectorGraph.Edge',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='src', full_name='VectorGraph.Edge.src', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dst', full_name='VectorGraph.Edge.dst', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=591,
  serialized_end=623,
)

_VECTORGRAPH_UINT32ATTRIBUTEVECTOR = _descriptor.Descriptor(
  name='UInt32AttributeVector',
  full_name='VectorGraph.UInt32AttributeVector',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='VectorGraph.UInt32AttributeVector.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target', full_name='VectorGraph.UInt32AttributeVector.target', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='values', full_name='VectorGraph.UInt32AttributeVector.values', index=2,
      number=3, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=625,
  serialized_end=728,
)

_VECTORGRAPH_INT32ATTRIBUTEVECTOR = _descriptor.Descriptor(
  name='Int32AttributeVector',
  full_name='VectorGraph.Int32AttributeVector',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='VectorGraph.Int32AttributeVector.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target', full_name='VectorGraph.Int32AttributeVector.target', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='values', full_name='VectorGraph.Int32AttributeVector.values', index=2,
      number=3, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=730,
  serialized_end=832,
)

_VECTORGRAPH_INT64ATTRIBUTEVECTOR = _descriptor.Descriptor(
  name='Int64AttributeVector',
  full_name='VectorGraph.Int64AttributeVector',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='VectorGraph.Int64AttributeVector.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target', full_name='VectorGraph.Int64AttributeVector.target', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='values', full_name='VectorGraph.Int64AttributeVector.values', index=2,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=834,
  serialized_end=936,
)

_VECTORGRAPH_FLOATATTRIBUTEVECTOR = _descriptor.Descriptor(
  name='FloatAttributeVector',
  full_name='VectorGraph.FloatAttributeVector',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='VectorGraph.FloatAttributeVector.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target', full_name='VectorGraph.FloatAttributeVector.target', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='values', full_name='VectorGraph.FloatAttributeVector.values', index=2,
      number=3, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=938,
  serialized_end=1040,
)

_VECTORGRAPH_DOUBLEATTRIBUTEVECTOR = _descriptor.Descriptor(
  name='DoubleAttributeVector',
  full_name='VectorGraph.DoubleAttributeVector',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='VectorGraph.DoubleAttributeVector.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target', full_name='VectorGraph.DoubleAttributeVector.target', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='values', full_name='VectorGraph.DoubleAttributeVector.values', index=2,
      number=3, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1042,
  serialized_end=1145,
)

_VECTORGRAPH_STRINGATTRIBUTEVECTOR = _descriptor.Descriptor(
  name='StringAttributeVector',
  full_name='VectorGraph.StringAttributeVector',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='VectorGraph.StringAttributeVector.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target', full_name='VectorGraph.StringAttributeVector.target', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='values', full_name='VectorGraph.StringAttributeVector.values', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1147,
  serialized_end=1246,
)

_VECTORGRAPH_BOOLATTRIBUTEVECTOR = _descriptor.Descriptor(
  name='BoolAttributeVector',
  full_name='VectorGraph.BoolAttributeVector',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='VectorGraph.BoolAttributeVector.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target', full_name='VectorGraph.BoolAttributeVector.target', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='values', full_name='VectorGraph.BoolAttributeVector.values', index=2,
      number=3, type=8, cpp_type=7, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1248,
  serialized_end=1349,
)

_VECTORGRAPH = _descriptor.Descriptor(
  name='VectorGraph',
  full_name='VectorGraph',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='VectorGraph.version', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='VectorGraph.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='VectorGraph.type', index=2,
      number=3, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vertexCount', full_name='VectorGraph.vertexCount', index=3,
      number=4, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='edgeCount', full_name='VectorGraph.edgeCount', index=4,
      number=5, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='edges', full_name='VectorGraph.edges', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uint32_vectors', full_name='VectorGraph.uint32_vectors', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='double_vectors', full_name='VectorGraph.double_vectors', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='string_vectors', full_name='VectorGraph.string_vectors', index=8,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='int32_vectors', full_name='VectorGraph.int32_vectors', index=9,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='int64_vectors', full_name='VectorGraph.int64_vectors', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='float_vectors', full_name='VectorGraph.float_vectors', index=11,
      number=12, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bool_vectors', full_name='VectorGraph.bool_vectors', index=12,
      number=13, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_VECTORGRAPH_EDGE, _VECTORGRAPH_UINT32ATTRIBUTEVECTOR, _VECTORGRAPH_INT32ATTRIBUTEVECTOR, _VECTORGRAPH_INT64ATTRIBUTEVECTOR, _VECTORGRAPH_FLOATATTRIBUTEVECTOR, _VECTORGRAPH_DOUBLEATTRIBUTEVECTOR, _VECTORGRAPH_STRINGATTRIBUTEVECTOR, _VECTORGRAPH_BOOLATTRIBUTEVECTOR, ],
  enum_types=[
    _VECTORGRAPH_GRAPHTYPE,
    _VECTORGRAPH_ATTRIBUTETARGET,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=1433,
)

_VECTORGRAPH_EDGE.containing_type = _VECTORGRAPH
_VECTORGRAPH_UINT32ATTRIBUTEVECTOR.fields_by_name['target'].enum_type = _VECTORGRAPH_ATTRIBUTETARGET
_VECTORGRAPH_UINT32ATTRIBUTEVECTOR.containing_type = _VECTORGRAPH
_VECTORGRAPH_INT32ATTRIBUTEVECTOR.fields_by_name['target'].enum_type = _VECTORGRAPH_ATTRIBUTETARGET
_VECTORGRAPH_INT32ATTRIBUTEVECTOR.containing_type = _VECTORGRAPH
_VECTORGRAPH_INT64ATTRIBUTEVECTOR.fields_by_name['target'].enum_type = _VECTORGRAPH_ATTRIBUTETARGET
_VECTORGRAPH_INT64ATTRIBUTEVECTOR.containing_type = _VECTORGRAPH
_VECTORGRAPH_FLOATATTRIBUTEVECTOR.fields_by_name['target'].enum_type = _VECTORGRAPH_ATTRIBUTETARGET
_VECTORGRAPH_FLOATATTRIBUTEVECTOR.containing_type = _VECTORGRAPH
_VECTORGRAPH_DOUBLEATTRIBUTEVECTOR.fields_by_name['target'].enum_type = _VECTORGRAPH_ATTRIBUTETARGET
_VECTORGRAPH_DOUBLEATTRIBUTEVECTOR.containing_type = _VECTORGRAPH
_VECTORGRAPH_STRINGATTRIBUTEVECTOR.fields_by_name['target'].enum_type = _VECTORGRAPH_ATTRIBUTETARGET
_VECTORGRAPH_STRINGATTRIBUTEVECTOR.containing_type = _VECTORGRAPH
_VECTORGRAPH_BOOLATTRIBUTEVECTOR.fields_by_name['target'].enum_type = _VECTORGRAPH_ATTRIBUTETARGET
_VECTORGRAPH_BOOLATTRIBUTEVECTOR.containing_type = _VECTORGRAPH
_VECTORGRAPH.fields_by_name['type'].enum_type = _VECTORGRAPH_GRAPHTYPE
_VECTORGRAPH.fields_by_name['edges'].message_type = _VECTORGRAPH_EDGE
_VECTORGRAPH.fields_by_name['uint32_vectors'].message_type = _VECTORGRAPH_UINT32ATTRIBUTEVECTOR
_VECTORGRAPH.fields_by_name['double_vectors'].message_type = _VECTORGRAPH_DOUBLEATTRIBUTEVECTOR
_VECTORGRAPH.fields_by_name['string_vectors'].message_type = _VECTORGRAPH_STRINGATTRIBUTEVECTOR
_VECTORGRAPH.fields_by_name['int32_vectors'].message_type = _VECTORGRAPH_INT32ATTRIBUTEVECTOR
_VECTORGRAPH.fields_by_name['int64_vectors'].message_type = _VECTORGRAPH_INT64ATTRIBUTEVECTOR
_VECTORGRAPH.fields_by_name['float_vectors'].message_type = _VECTORGRAPH_FLOATATTRIBUTEVECTOR
_VECTORGRAPH.fields_by_name['bool_vectors'].message_type = _VECTORGRAPH_BOOLATTRIBUTEVECTOR
_VECTORGRAPH_GRAPHTYPE.containing_type = _VECTORGRAPH
_VECTORGRAPH_ATTRIBUTETARGET.containing_type = _VECTORGRAPH
DESCRIPTOR.message_types_by_name['VectorGraph'] = _VECTORGRAPH

VectorGraph = _reflection.GeneratedProtocolMessageType('VectorGraph', (_message.Message,), dict(

  Edge = _reflection.GeneratedProtocolMessageType('Edge', (_message.Message,), dict(
    DESCRIPTOR = _VECTORGRAPH_EDGE,
    __module__ = 'graph_vector_pb2'
    # @@protoc_insertion_point(class_scope:VectorGraph.Edge)
    ))
  ,

  UInt32AttributeVector = _reflection.GeneratedProtocolMessageType('UInt32AttributeVector', (_message.Message,), dict(
    DESCRIPTOR = _VECTORGRAPH_UINT32ATTRIBUTEVECTOR,
    __module__ = 'graph_vector_pb2'
    # @@protoc_insertion_point(class_scope:VectorGraph.UInt32AttributeVector)
    ))
  ,

  Int32AttributeVector = _reflection.GeneratedProtocolMessageType('Int32AttributeVector', (_message.Message,), dict(
    DESCRIPTOR = _VECTORGRAPH_INT32ATTRIBUTEVECTOR,
    __module__ = 'graph_vector_pb2'
    # @@protoc_insertion_point(class_scope:VectorGraph.Int32AttributeVector)
    ))
  ,

  Int64AttributeVector = _reflection.GeneratedProtocolMessageType('Int64AttributeVector', (_message.Message,), dict(
    DESCRIPTOR = _VECTORGRAPH_INT64ATTRIBUTEVECTOR,
    __module__ = 'graph_vector_pb2'
    # @@protoc_insertion_point(class_scope:VectorGraph.Int64AttributeVector)
    ))
  ,

  FloatAttributeVector = _reflection.GeneratedProtocolMessageType('FloatAttributeVector', (_message.Message,), dict(
    DESCRIPTOR = _VECTORGRAPH_FLOATATTRIBUTEVECTOR,
    __module__ = 'graph_vector_pb2'
    # @@protoc_insertion_point(class_scope:VectorGraph.FloatAttributeVector)
    ))
  ,

  DoubleAttributeVector = _reflection.GeneratedProtocolMessageType('DoubleAttributeVector', (_message.Message,), dict(
    DESCRIPTOR = _VECTORGRAPH_DOUBLEATTRIBUTEVECTOR,
    __module__ = 'graph_vector_pb2'
    # @@protoc_insertion_point(class_scope:VectorGraph.DoubleAttributeVector)
    ))
  ,

  StringAttributeVector = _reflection.GeneratedProtocolMessageType('StringAttributeVector', (_message.Message,), dict(
    DESCRIPTOR = _VECTORGRAPH_STRINGATTRIBUTEVECTOR,
    __module__ = 'graph_vector_pb2'
    # @@protoc_insertion_point(class_scope:VectorGraph.StringAttributeVector)
    ))
  ,

  BoolAttributeVector = _reflection.GeneratedProtocolMessageType('BoolAttributeVector', (_message.Message,), dict(
    DESCRIPTOR = _VECTORGRAPH_BOOLATTRIBUTEVECTOR,
    __module__ = 'graph_vector_pb2'
    # @@protoc_insertion_point(class_scope:VectorGraph.BoolAttributeVector)
    ))
  ,
  DESCRIPTOR = _VECTORGRAPH,
  __module__ = 'graph_vector_pb2'
  # @@protoc_insertion_point(class_scope:VectorGraph)
  ))
_sym_db.RegisterMessage(VectorGraph)
_sym_db.RegisterMessage(VectorGraph.Edge)
_sym_db.RegisterMessage(VectorGraph.UInt32AttributeVector)
_sym_db.RegisterMessage(VectorGraph.Int32AttributeVector)
_sym_db.RegisterMessage(VectorGraph.Int64AttributeVector)
_sym_db.RegisterMessage(VectorGraph.FloatAttributeVector)
_sym_db.RegisterMessage(VectorGraph.DoubleAttributeVector)
_sym_db.RegisterMessage(VectorGraph.StringAttributeVector)
_sym_db.RegisterMessage(VectorGraph.BoolAttributeVector)


_VECTORGRAPH_UINT32ATTRIBUTEVECTOR.fields_by_name['values'].has_options = True
_VECTORGRAPH_UINT32ATTRIBUTEVECTOR.fields_by_name['values']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_VECTORGRAPH_INT32ATTRIBUTEVECTOR.fields_by_name['values'].has_options = True
_VECTORGRAPH_INT32ATTRIBUTEVECTOR.fields_by_name['values']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_VECTORGRAPH_INT64ATTRIBUTEVECTOR.fields_by_name['values'].has_options = True
_VECTORGRAPH_INT64ATTRIBUTEVECTOR.fields_by_name['values']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_VECTORGRAPH_FLOATATTRIBUTEVECTOR.fields_by_name['values'].has_options = True
_VECTORGRAPH_FLOATATTRIBUTEVECTOR.fields_by_name['values']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_VECTORGRAPH_DOUBLEATTRIBUTEVECTOR.fields_by_name['values'].has_options = True
_VECTORGRAPH_DOUBLEATTRIBUTEVECTOR.fields_by_name['values']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_VECTORGRAPH_BOOLATTRIBUTEVECTOR.fields_by_name['values'].has_options = True
_VECTORGRAPH_BOOLATTRIBUTEVECTOR.fields_by_name['values']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
# @@protoc_insertion_point(module_scope)
