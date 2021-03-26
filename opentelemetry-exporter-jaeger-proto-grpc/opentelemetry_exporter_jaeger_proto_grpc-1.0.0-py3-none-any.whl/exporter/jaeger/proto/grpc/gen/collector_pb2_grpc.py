# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import collector_pb2 as collector__pb2


class CollectorServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.PostSpans = channel.unary_unary(
        '/jaeger.api_v2.CollectorService/PostSpans',
        request_serializer=collector__pb2.PostSpansRequest.SerializeToString,
        response_deserializer=collector__pb2.PostSpansResponse.FromString,
        )


class CollectorServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def PostSpans(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_CollectorServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'PostSpans': grpc.unary_unary_rpc_method_handler(
          servicer.PostSpans,
          request_deserializer=collector__pb2.PostSpansRequest.FromString,
          response_serializer=collector__pb2.PostSpansResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'jaeger.api_v2.CollectorService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
