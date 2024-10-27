<html>
	<center>Distributed Architectures and Programming</center>
	<center>ISEP - October 2024</center>
	<center style="font-style:italic">by Quentin LAURENT and Theophile WEMAERE</center>
</html>

> [!NOTE]
> The source code of this lab can also be found on Github :
> https://github.com/Theophile-Wemaere/ArchProgDistr

# Task: Implement error handling for invalid inputs in the AddBook method

Here, we simply implemented a check on the server side to ensure that, when creating a new `Book`, both the `title` and the `author`are not empty strings.

**Server's code:**

```python
from concurrent import futures  
  
import grpc  
import book_pb2  
import book_pb2_grpc  
  
class BookService(book_pb2_grpc.BookServiceServicer):  
    def __init__(self):  
        self.books = [  
            book_pb2.Book(id=1, title="1984", author="George Orwell"),  
            book_pb2.Book(id=2, title="To Kill a Mockingbird", author="Harper Lee"),  
        ]  
        self.next_id = 3  
  
    def GetBook(self, request, context):  
        for book in self.books:  
            if book.id == request.id:  
                return book_pb2.BookResponse(book=book)  
        context.set_code(grpc.StatusCode.NOT_FOUND)  
        context.set_details('Book not found')  
        return book_pb2.BookResponse()  
  
    def ListBooks(self, request, context):  
        return book_pb2.BookListResponse(books=self.books)  
  
    def AddBook(self, request, context):  
        title, author = request.title, request.author  
  
        # Error handling: prevent creating books with an empty title/author  
        if len(title) < 1:  
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)  
            context.set_details("Book title cannot be empty.")  
            return book_pb2.BookResponse()  
        elif len(author) < 1:  
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)  
            context.set_details("Book title cannot be empty.")  
            return book_pb2.BookResponse()  
  
        new_book = book_pb2.Book(id=self.next_id, title=title, author=author)  
        self.books.append(new_book)  
        self.next_id += 1  
        return book_pb2.BookResponse(book=new_book)  
  
def serve():  
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  
    book_pb2_grpc.add_BookServiceServicer_to_server(BookService(), server)  
    server.add_insecure_port('[::]:50051')  
    server.start()  
    print("Server started on port 50051")  
    server.wait_for_termination()  
  
if  __name__ == '__main__':  
    try:  
        serve()  
    except KeyboardInterrupt:  
        print("Exiting... (Ctrl+C)")
```

<div style="page-break-after: always;"></div>

**Client's code:**

```python
import grpc  
import book_pb2  
import book_pb2_grpc  
  
def run():  
    with grpc.insecure_channel('localhost:50051') as channel:  
        stub = book_pb2_grpc.BookServiceStub(channel)  
        # Get a single book by ID  
        try:  
            response = stub.GetBook(book_pb2.BookRequest(id=1))  
            print(f"Book: {response.book.title} by {response.book.author}")  
        except grpc.RpcError as e:  
            print(f"Error: {e.details()}")  
  
        # List all books  
        books = stub.ListBooks(book_pb2.Empty())  
        print(books)  
  
        for book in books.books:  
            print(f"Book: {book.title} by {book.author}")  
  
        new_book_response = stub.AddBook(book_pb2.NewBookRequest(title="Brave New World",author="Aldous Huxley"))  
        print(f"Added Book: {new_book_response.book.title} by {new_book_response.book.author}")  
  
        # Try to add a book with an empty title/author  
        try:  
            new_book_response = stub.AddBook(book_pb2.NewBookRequest(title="", author=""))  
        except grpc.RpcError as e:  
            print(f"Error when trying to add book: {e.details()}")  
  
        new_book_response = stub.AddBook(book_pb2.NewBookRequest(title="L'Etranger", author="Albert Camus"))  
  
        print(f"Added Book: {new_book_response.book.title} by {new_book_response.book.author}")  
  
if __name__ == '__main__':  
    run()
```

<div style="page-break-after: always;"></div>

# Task: Calculator Service implementation

*Using gRPC implement Calculator Service. This service allows clients to:*
*- Add two numbers*
*- Subtract one number from another*
*- Multiply two numbers*
*- Divide two numbers*

*All operations (Add, Subtract, Multiply, Divide) are unary RPCs, which send
one request and receive one response.
Error Handling: Division by zero should be handled gracefully.*

To create this service, we started by creating the `.proto` file with all the required gRPC requests and responses classes:

**`calculator.proto`'s code:**

```protobuf
syntax = "proto3";  
  
package calculator;  
  
service CalculatorService {  
    // Add two numbers  
    rpc Add(AddRequest) returns (AddResponse);  
    // Subtract two numbers  
    rpc Subtract(SubtractRequest) returns (SubtractResponse);  
    // Multiply two numbers  
    rpc Multiply(MultiplyRequest) returns (MultiplyResponse);  
    // Divide two numbers  
    rpc Divide(DivideRequest) returns (DivideResponse);  
}  
  
// Request to add two numbers  
message AddRequest {  
    int32 first_number = 1;  
    int32 second_number = 2;  
}  
  
// Request to subtract two numbers  
message SubtractRequest {  
    int32 first_number = 1;  
    int32 second_number = 2;  
}  
  
// Request to multiply two numbers  
message MultiplyRequest {  
    int32 first_number = 1;  
    int32 second_number = 2;  
}  
  
// Request to divide two numbers  
message DivideRequest {  
    int32 first_number = 1;  
    int32 second_number = 2;  
}  
  
message AddResponse {  
    int32 result = 1;  
}  
  
message SubtractResponse {  
    int32 result = 1;  
}  
  
message MultiplyResponse {  
    int32 result = 1;  
}  
  
message DivideResponse {  
    float result = 1;  
}
```

We can then generate the required files using the following command:

```bash
python3 -m grpc_tools.protoc -I . --python_out=. --pyi_out=. --grpc_python_out=. calculator.proto
```

Finally, we just had to implement a server implementing the `CalculatorService` as well as a client invoking functions from the server.

We made sure to implement exception handling in the `Divide` function by returning an appropriate error when a division by zero occurs.

<div style="page-break-after: always;"></div>

**Server's code:**

```python
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
```

<div style="page-break-after: always;"></div>

**Client's code:**

```python
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
```
