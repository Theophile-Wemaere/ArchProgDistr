import grpc

import calculator_pb2
import calculator_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculator_pb2_grpc.CalculatorServiceStub(channel)

        # Add two numbers
        result = stub.Add(calculator_pb2.AddRequest(first_number=5, second_number=8))
        print(f"Result of 5+8 = {result}")

        # Subtract two numbers
        result = stub.Subtract(calculator_pb2.SubtractRequest(first_number=5, second_number=8))
        print(f"Result of 5-8 = {result}")

        # Multiply two numbers
        result = stub.Multiply(calculator_pb2.MultiplyRequest(first_number=5, second_number=8))
        print(f"Result of 5*8 = {result}")

        # Divide two numbers
        try:
            result = stub.Divide(calculator_pb2.DivideRequest(first_number=5, second_number=8))
            print(f"Result of 5/8 = {result}")
        except grpc.RpcError as e:
            print(f"Result of 5/0 = {e.details()}")

        try:
            result = stub.Divide(calculator_pb2.DivideRequest(first_number=5, second_number=0))
            print(f"Result of 5/0 = {result}")
        except grpc.RpcError as e:
            print(f"Result of 5/0 = {e.details()}")


if __name__ == '__main__':
    run()

