#! usr/bin/python
import socket
import sys


def echo_client(message):
    CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    CLIENT_SOCKET.connect(('127.0.0.1', 50000))
    if type(message) == unicode:
        message = message.encode('UTF-8')
    CLIENT_SOCKET.sendall(message)
   # if not sys.getsizeof(message) % 32:
   #             CLIENT_SOCKET.send()
    CLIENT_SOCKET.shutdown(socket.SHUT_WR)
    buffsize = 32
    done = False
    complete_msg = ''
    while not done:
        rcvd_msg_part = CLIENT_SOCKET.recv(buffsize)
        complete_msg += rcvd_msg_part
        if len(rcvd_msg_part) < buffsize:
            done = True
    CLIENT_SOCKET.close()
    print(complete_msg)
    return complete_msg

if __name__ == '__main__':
    try:
        echo_client(sys.argv[1])
    except IndexError:
        print('Please enter a message')
