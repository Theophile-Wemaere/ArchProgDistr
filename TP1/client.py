import socket
import sys

pseudo = "Theo"

def main():

    if len(sys.argv) < 3:
        print("use ./client.py HOST PORT")
        exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            msg = input("Message : ")
            s.sendall(str.encode(pseudo+":"+msg))
            data = s.recv(1024)
            print('Received',repr(data))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)