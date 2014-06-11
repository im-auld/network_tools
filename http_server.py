import socket

def request_parser(request):
  #  import pdb; pdb.set_trace()
    request = request.replace("\r\n", " ").split(" ")
    if len(request) <= 5:
        raise IndexError
    method, URI, protocol, host_key, host = request[:5]
    if method != "GET":
        raise AttributeError
    if URI[0] != "/":
        raise SyntaxError
    if protocol.strip() != "HTTP/1.1":
        raise NameError
    if host_key not in ("Host:"):
        raise ValueError
    return URI


def http_server():
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
        try:
            URI = request_parser(final_output)
            response = "200 OK: Your URI is {}".format(URI)
        except IndexError:
            response = "400 Bad Request"
        except AttributeError:
            response = "405 Method Not Allowed"
        except SyntaxError:
            response = "404 Not Found"
        except NameError:
            response = "400 Bad Request"
        except ValueError:
            response = "404 Not Found"
        conn.sendall(response)
        conn.close()
       # if final_output:
        #    break
    SERVER_SOCKET.close()
    return final_output


if __name__ == '__main__':
    http_server()
