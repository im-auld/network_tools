import socket
from HTTPExceptions import HTTPException , HTTP400Error, HTTP404Error, HTTP405Error


def request_parser(raw_request):
    raw_request = raw_request.split('\r\n')
    keys = ('method', 'URI', 'protocol')
    request = dict(zip(keys, raw_request[0].split()))
    for element in raw_request[1:]:
        if element.lower().startswith('host:'):
            request['host'] = element.split()[1]
            break
    return request

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

def request_validator(request):
    try:
        check_request_method(request)
        check_request_URI(request)
        check_request_protocol(request)
        check_request_host(request)
        return ('200', 'OK', 'This is a message')
    except HTTPException as err:
        return (err.code, err.message, '<h1>{} - {}</h1>'.format(err.code, err.message))
    # except HTTP404Error as err:
    #     response = RESPONSE.format(404, err.message, '')
    # except HTTP405Error as err:
    #     response = RESPONSE.format(405, err.message, '')

def response_builder(response):
    template = '\r\n'.join(['HTTP/1.1 {} {}', 'Content-Type: text/plain', '', '{}'])
    return template.format(*response)

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
        request = request_parser(final_output)
        #import pdb; pdb.set_trace()
        response = request_validator(request)
        response = response_builder(response)
        conn.sendall(response)
        conn.close()
    SERVER_SOCKET.close()
    return final_output


if __name__ == '__main__':
    http_server()
