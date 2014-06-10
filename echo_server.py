#! usr/bin/python
import socket
import sys


def echo_server():
    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SERVER_SOCKET.bind(('127.0.0.1', 50000))
    print('Waiting for message...')
    while True:
        final_output = ''
        done = False
        buffsize = 32
        SERVER_SOCKET.listen(1)
        conn, addr = SERVER_SOCKET.accept()
        while not done:
            msg_part = conn.recv(buffsize)
            final_output += msg_part
            if len(msg_part) < buffsize:
                done = True
        conn.sendall(final_output)
        conn.close()
        if msg_part == "exit":
            break
    SERVER_SOCKET.close()
    return final_output


if __name__ == '__main__':
    echo_server()
