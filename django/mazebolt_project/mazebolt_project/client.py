import socket
import server_default


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('10.132.0.10', server_default.PORT))
        s.send(server_default.Message.ADD)
        print(s.recv(1024))


main()
