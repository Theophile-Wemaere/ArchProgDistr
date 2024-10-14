from xmlrpc.server import SimpleXMLRPCServer

# Define the functions that can be called remotely
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

def multiply_matrix(m1: list[list[int]], m2: list[list[int]]) -> list[list[int]]:
    print(f"[DEBUG] Resulting matrix will be of size {len(m2[0])}x{len(m1)}")
    # We use a double list comprehension to create an empty matrix of size M2_C x M1_L where:
    # M2_C is the number of columns of the M2 matrix
    # M1_L is the number of lines of the M1 matrix
    res = [[0 for _ in range(len(m2[0]))] for _ in range(len(m1))]

    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m2)):
                res[i][j] += m1[i][k] * m2[k][j]

    return res

# Create the server
server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")

# Register the functions
server.register_function(add, "add")
server.register_function(subtract, "subtract")
server.register_function(multiply, "multiply")
server.register_function(divide, "divide")
server.register_function(multiply_matrix, "multiply_matrix")

# Run the server
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
