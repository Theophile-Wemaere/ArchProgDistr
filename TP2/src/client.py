import xmlrpc.client
from xmlrpc.client import Fault

# Create a proxy for the server
server = xmlrpc.client.ServerProxy("http://localhost:8000/")

# Call the remote functions
print("Addition of 5 and 3:", server.add(5, 3))
print("Subtraction of 8 and 2:", server.subtract(8, 2))
print("Multiplication of 3 and 8:", server.multiply(3, 8))

# For the division function, we surround the funtion call in a try/catch
# so that we can catch any eventual error raised during a division
# (i.e. a division by zero)
try:
    print("Division of 5 and 0:", server.divide(5, 0))
except Fault as fault:
    print(f"Division of 5 and 0: {fault.faultString}")

# Matrix multiplication
m1 = [[12, 7, 3],
      [4, 5, 6],
      [7, 8, 9]]

m2 = [[5, 8, 1, 2],
      [6, 7, 3, 0],
      [4, 5, 9 ,1]]

res = server.multiply_matrix(m1, m2)

print("Matrix multiplication of m1 and m2:")
for row in res:
    print(row)
