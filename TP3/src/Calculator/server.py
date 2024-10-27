from concurrent import futures

import grpc
import calculator_pb2
import calculator_pb2_grpc

class CalculatorService(calculator_pb2_grpc.CalculatorServiceServicer):
    def __init__(self):
        return

    def Add(self, request, context):
        first_number, second_number = request.first_number, request.second_number
        result = first_number + second_number
        return calculator_pb2.AddResponse(result=result)

    def Subtract(self, request, context):
        first_number, second_number = request.first_number, request.second_number
        result = first_number - second_number
        return calculator_pb2.SubtractResponse(result=result)

    def Multiply(self, request, context):
        first_number, second_number = request.first_number, request.second_number
        result = first_number * second_number
        return calculator_pb2.MultiplyResponse(result=result)

    def Divide(self, request, context):
        first_number, second_number = request.first_number, request.second_number
        try:
            result = first_number / second_number
            return calculator_pb2.DivideResponse(result=result)
        except ZeroDivisionError:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Cannot divide {first_number} by zero.')
        return calculator_pb2.DivideResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServiceServicer_to_server(CalculatorService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if  __name__ == '__main__':
    try:
        serve()
    except KeyboardInterrupt:
        print("Exiting... (Ctrl+C)")
