import socket
from HTTPExceptions import HTTP400Error, HTTP404Error, HTTP405Error


RESPONSE = '\r\n'.join(['HTTP/1.1 {} {}', 'Content-Type: text/plain', '', '{}'])


def request_parser(raw_request):
    #import pdb; pdb.set_trace()
    raw_request = raw_request.split('\r\n')
    keys = ('method', 'URI', 'protocol')
    request = dict(zip(keys, raw_request[0].split()))
    for element in raw_request[1:]:
        if element.lower().startswith('host:'):
            request['host'] = element.split()[1]
            break
    if len(request) == 4:
        return request
    else:
        raise HTTP400Error('Bad Request')
    
def check_request_method(request):
    if request['method'] != 'GET':
        raise HTTP405Error('Method Not Allowed')
    
def check_request_URI(request):
    if not request['URI'].startswith('/'):
        raise HTTP400Error('Bad Request')
    
def check_request_protocol(request):
    if request['protocol'] != "HTTP/1.1":
        raise HTTP400Error('Bad Request')
    
def check_request_host(request):
    if 'host' not in request:
        raise HTTP400Error('Bad Request')

def http_server():
    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SERVER_SOCKET.bind(('127.0.0.1', 50000))
    buffsize = 32
    SERVER_SOCKET.listen(1)
    print('Waiting for message...')
    while True:
        final_output = ''
        done = False
        conn, addr = SERVER_SOCKET.accept()
        while not done:
            msg_part = conn.recv(buffsize)
            final_output += msg_part
            if len(msg_part) < buffsize:
                done = True
        try:
            request = request_parser(final_output)
            check_request_method(request)
            check_request_URI(request)
            check_request_protocol(request)
            check_request_host(request)
            response = RESPONSE.format('200', 'OK', 'This a message')
        except HTTP400Error as err:
            response = RESPONSE.format(400, err.message, '')
        except HTTP404Error as err:
            response = RESPONSE.format(404, err.message, '')
        except HTTP405Error as err:
            response = RESPONSE.format(405, err.message, '')
        conn.sendall(response)
        conn.close()
       # if final_output:
        #    break
    SERVER_SOCKET.close()
    return final_output


if __name__ == '__main__':
    http_server()
