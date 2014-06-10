#! usr/bin/python
import socket
import sys


def echo_client(message):
    CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    CLIENT_SOCKET.connect(('127.0.0.1', 50000))
    if type(message) == unicode:
        message = message.encode('UTF-8')
    CLIENT_SOCKET.sendall(message)
    CLIENT_SOCKET.shutdown(socket.SHUT_WR)
    received_msg = CLIENT_SOCKET.recv(32)
    CLIENT_SOCKET.close()
    print(received_msg)
    return received_msg

if __name__ == '__main__':
    try:
        echo_client(sys.argv[1])
    except IndexError:
        print('Please enter a message')