# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import calculator_pb2 as calculator__pb2

GRPC_GENERATED_VERSION = '1.65.5'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.66.0'
SCHEDULED_RELEASE_DATE = 'August 6, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in calculator_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class CalculatorServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Add = channel.unary_unary(
                '/calculator.CalculatorService/Add',
                request_serializer=calculator__pb2.AddRequest.SerializeToString,
                response_deserializer=calculator__pb2.AddResponse.FromString,
                _registered_method=True)
        self.Subtract = channel.unary_unary(
                '/calculator.CalculatorService/Subtract',
                request_serializer=calculator__pb2.SubtractRequest.SerializeToString,
                response_deserializer=calculator__pb2.SubtractResponse.FromString,
                _registered_method=True)
        self.Multiply = channel.unary_unary(
                '/calculator.CalculatorService/Multiply',
                request_serializer=calculator__pb2.MultiplyRequest.SerializeToString,
                response_deserializer=calculator__pb2.MultiplyResponse.FromString,
                _registered_method=True)
        self.Divide = channel.unary_unary(
                '/calculator.CalculatorService/Divide',
                request_serializer=calculator__pb2.DivideRequest.SerializeToString,
                response_deserializer=calculator__pb2.DivideResponse.FromString,
                _registered_method=True)


class CalculatorServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Add(self, request, context):
        """Add two numbers
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Subtract(self, request, context):
        """Subtract two numbers
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Multiply(self, request, context):
        """Multiply two numbers
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Divide(self, request, context):
        """Divide two numbers
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CalculatorServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Add': grpc.unary_unary_rpc_method_handler(
                    servicer.Add,
                    request_deserializer=calculator__pb2.AddRequest.FromString,
                    response_serializer=calculator__pb2.AddResponse.SerializeToString,
            ),
            'Subtract': grpc.unary_unary_rpc_method_handler(
                    servicer.Subtract,
                    request_deserializer=calculator__pb2.SubtractRequest.FromString,
                    response_serializer=calculator__pb2.SubtractResponse.SerializeToString,
            ),
            'Multiply': grpc.unary_unary_rpc_method_handler(
                    servicer.Multiply,
                    request_deserializer=calculator__pb2.MultiplyRequest.FromString,
                    response_serializer=calculator__pb2.MultiplyResponse.SerializeToString,
            ),
            'Divide': grpc.unary_unary_rpc_method_handler(
                    servicer.Divide,
                    request_deserializer=calculator__pb2.DivideRequest.FromString,
                    response_serializer=calculator__pb2.DivideResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'calculator.CalculatorService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('calculator.CalculatorService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class CalculatorService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Add(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/calculator.CalculatorService/Add',
            calculator__pb2.AddRequest.SerializeToString,
            calculator__pb2.AddResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Subtract(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/calculator.CalculatorService/Subtract',
            calculator__pb2.SubtractRequest.SerializeToString,
            calculator__pb2.SubtractResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Multiply(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/calculator.CalculatorService/Multiply',
            calculator__pb2.MultiplyRequest.SerializeToString,
            calculator__pb2.MultiplyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Divide(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/calculator.CalculatorService/Divide',
            calculator__pb2.DivideRequest.SerializeToString,
            calculator__pb2.DivideResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
