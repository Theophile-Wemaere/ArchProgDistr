package com.isep.labgrpc;


import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.StatusRuntimeException;
import calculator.CalculatorServiceGrpc;
import calculator.Calculator.*;

public class CalculatorClient {

    public static void main(String[] args) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 50051)
                .usePlaintext()
                .build();

        CalculatorServiceGrpc.CalculatorServiceBlockingStub stub = CalculatorServiceGrpc.newBlockingStub(channel);

        AddRequest addRequest = AddRequest.newBuilder().setFirstNumber(5).setSecondNumber(8).build();
        AddResponse addResponse = stub.add(addRequest);
        System.out.println("Result of 5 + 8 = " + addResponse.getResult());

        SubtractRequest subtractRequest = SubtractRequest.newBuilder().setFirstNumber(5).setSecondNumber(8).build();
        SubtractResponse subtractResponse = stub.subtract(subtractRequest);
        System.out.println("Result of 5 - 8 = " + subtractResponse.getResult());

        MultiplyRequest multiplyRequest = MultiplyRequest.newBuilder().setFirstNumber(5).setSecondNumber(8).build();
        MultiplyResponse multiplyResponse = stub.multiply(multiplyRequest);
        System.out.println("Result of 5 * 8 = " + multiplyResponse.getResult());

        try {
            DivideRequest divideRequest = DivideRequest.newBuilder().setFirstNumber(5).setSecondNumber(8).build();
            DivideResponse divideResponse = stub.divide(divideRequest);
            System.out.println("Result of 5 / 8 = " + divideResponse.getResult());
        } catch (StatusRuntimeException e) {
            System.err.println("Failed to divide: " + e.getStatus().getDescription());
        }

        try {
            DivideRequest divideByZeroRequest = DivideRequest.newBuilder().setFirstNumber(5).setSecondNumber(0).build();
            DivideResponse divideByZeroResponse = stub.divide(divideByZeroRequest);
            System.out.println("Result of 5 / 0 = " + divideByZeroResponse.getResult());
        } catch (StatusRuntimeException e) {
            System.err.println("Failed to divide: " + e.getStatus().getDescription());
        } finally {
            channel.shutdown();
        }
    }
}
