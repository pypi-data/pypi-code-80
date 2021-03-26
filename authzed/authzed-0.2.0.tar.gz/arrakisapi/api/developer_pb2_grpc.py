# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from arrakisapi.api import developer_pb2 as arrakisapi_dot_api_dot_developer__pb2


class DeveloperServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Validate = channel.unary_unary(
                '/DeveloperService/Validate',
                request_serializer=arrakisapi_dot_api_dot_developer__pb2.ValidateRequest.SerializeToString,
                response_deserializer=arrakisapi_dot_api_dot_developer__pb2.ValidateResponse.FromString,
                )


class DeveloperServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Validate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DeveloperServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Validate': grpc.unary_unary_rpc_method_handler(
                    servicer.Validate,
                    request_deserializer=arrakisapi_dot_api_dot_developer__pb2.ValidateRequest.FromString,
                    response_serializer=arrakisapi_dot_api_dot_developer__pb2.ValidateResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'DeveloperService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DeveloperService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Validate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DeveloperService/Validate',
            arrakisapi_dot_api_dot_developer__pb2.ValidateRequest.SerializeToString,
            arrakisapi_dot_api_dot_developer__pb2.ValidateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
