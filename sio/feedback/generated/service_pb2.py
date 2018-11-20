# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto

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
  name='service.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\rservice.proto\"\x07\n\x05\x45mpty\"&\n\x10\x43ompilationStart\x12\x12\n\njudging_id\x18\x01 \x01(\x03\"]\n\x11\x43ompilationResult\x12\x12\n\njudging_id\x18\x01 \x01(\x03\x12\x18\n\x10\x63ompilation_code\x18\x03 \x01(\t\x12\x1a\n\x12\x63ompilation_output\x18\x04 \x01(\t\"3\n\nJudgeStart\x12\x12\n\njudging_id\x18\x01 \x01(\x03\x12\x11\n\ttest_name\x18\x02 \x01(\t\"/\n\x14JudgePrepareResponse\x12\x17\n\x0f\x66orce_not_judge\x18\x01 \x01(\x08\"I\n\x0bJudgeFinish\x12\x12\n\njudging_id\x18\x01 \x01(\x03\x12\x11\n\ttest_name\x18\x02 \x01(\t\x12\x13\n\x0bstatus_code\x18\x03 \x01(\t2\xf5\x01\n\x0f\x46\x65\x65\x64\x62\x61\x63kService\x12/\n\x12\x43ompilationStarted\x12\x11.CompilationStart\x1a\x06.Empty\x12\x31\n\x13\x43ompilationFinished\x12\x12.CompilationResult\x1a\x06.Empty\x12\x32\n\x0cJudgePrepare\x12\x0b.JudgeStart\x1a\x15.JudgePrepareResponse\x12#\n\x0cJudgeStarted\x12\x0b.JudgeStart\x1a\x06.Empty\x12%\n\rJudgeFinished\x12\x0c.JudgeFinish\x1a\x06.Emptyb\x06proto3')
)




_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=24,
)


_COMPILATIONSTART = _descriptor.Descriptor(
  name='CompilationStart',
  full_name='CompilationStart',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='judging_id', full_name='CompilationStart.judging_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=26,
  serialized_end=64,
)


_COMPILATIONRESULT = _descriptor.Descriptor(
  name='CompilationResult',
  full_name='CompilationResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='judging_id', full_name='CompilationResult.judging_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='compilation_code', full_name='CompilationResult.compilation_code', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='compilation_output', full_name='CompilationResult.compilation_output', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=66,
  serialized_end=159,
)


_JUDGESTART = _descriptor.Descriptor(
  name='JudgeStart',
  full_name='JudgeStart',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='judging_id', full_name='JudgeStart.judging_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='test_name', full_name='JudgeStart.test_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=161,
  serialized_end=212,
)


_JUDGEPREPARERESPONSE = _descriptor.Descriptor(
  name='JudgePrepareResponse',
  full_name='JudgePrepareResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='force_not_judge', full_name='JudgePrepareResponse.force_not_judge', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=214,
  serialized_end=261,
)


_JUDGEFINISH = _descriptor.Descriptor(
  name='JudgeFinish',
  full_name='JudgeFinish',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='judging_id', full_name='JudgeFinish.judging_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='test_name', full_name='JudgeFinish.test_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status_code', full_name='JudgeFinish.status_code', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=263,
  serialized_end=336,
)

DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['CompilationStart'] = _COMPILATIONSTART
DESCRIPTOR.message_types_by_name['CompilationResult'] = _COMPILATIONRESULT
DESCRIPTOR.message_types_by_name['JudgeStart'] = _JUDGESTART
DESCRIPTOR.message_types_by_name['JudgePrepareResponse'] = _JUDGEPREPARERESPONSE
DESCRIPTOR.message_types_by_name['JudgeFinish'] = _JUDGEFINISH
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:Empty)
  ))
_sym_db.RegisterMessage(Empty)

CompilationStart = _reflection.GeneratedProtocolMessageType('CompilationStart', (_message.Message,), dict(
  DESCRIPTOR = _COMPILATIONSTART,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:CompilationStart)
  ))
_sym_db.RegisterMessage(CompilationStart)

CompilationResult = _reflection.GeneratedProtocolMessageType('CompilationResult', (_message.Message,), dict(
  DESCRIPTOR = _COMPILATIONRESULT,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:CompilationResult)
  ))
_sym_db.RegisterMessage(CompilationResult)

JudgeStart = _reflection.GeneratedProtocolMessageType('JudgeStart', (_message.Message,), dict(
  DESCRIPTOR = _JUDGESTART,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:JudgeStart)
  ))
_sym_db.RegisterMessage(JudgeStart)

JudgePrepareResponse = _reflection.GeneratedProtocolMessageType('JudgePrepareResponse', (_message.Message,), dict(
  DESCRIPTOR = _JUDGEPREPARERESPONSE,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:JudgePrepareResponse)
  ))
_sym_db.RegisterMessage(JudgePrepareResponse)

JudgeFinish = _reflection.GeneratedProtocolMessageType('JudgeFinish', (_message.Message,), dict(
  DESCRIPTOR = _JUDGEFINISH,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:JudgeFinish)
  ))
_sym_db.RegisterMessage(JudgeFinish)



_FEEDBACKSERVICE = _descriptor.ServiceDescriptor(
  name='FeedbackService',
  full_name='FeedbackService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=339,
  serialized_end=584,
  methods=[
  _descriptor.MethodDescriptor(
    name='CompilationStarted',
    full_name='FeedbackService.CompilationStarted',
    index=0,
    containing_service=None,
    input_type=_COMPILATIONSTART,
    output_type=_EMPTY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='CompilationFinished',
    full_name='FeedbackService.CompilationFinished',
    index=1,
    containing_service=None,
    input_type=_COMPILATIONRESULT,
    output_type=_EMPTY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='JudgePrepare',
    full_name='FeedbackService.JudgePrepare',
    index=2,
    containing_service=None,
    input_type=_JUDGESTART,
    output_type=_JUDGEPREPARERESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='JudgeStarted',
    full_name='FeedbackService.JudgeStarted',
    index=3,
    containing_service=None,
    input_type=_JUDGESTART,
    output_type=_EMPTY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='JudgeFinished',
    full_name='FeedbackService.JudgeFinished',
    index=4,
    containing_service=None,
    input_type=_JUDGEFINISH,
    output_type=_EMPTY,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_FEEDBACKSERVICE)

DESCRIPTOR.services_by_name['FeedbackService'] = _FEEDBACKSERVICE

# @@protoc_insertion_point(module_scope)

