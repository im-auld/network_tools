#! usr/bin/python
import socket


def echo_server():
    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SERVER_SOCKET.bind(('127.0.0.1', 50000))
    print('Waiting for message...')
    while True:
        SERVER_SOCKET.listen(1)
        conn, addr = SERVER_SOCKET.accept()
        received_msg = conn.recv(32)
        if received_msg != '^D':
            conn.sendall(received_msg)
        else:
            break
        conn.close()
    SERVER_SOCKET.close()
    return received_msg


if __name__ == '__main__':
    echo_server()