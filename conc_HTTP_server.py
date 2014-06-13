import socket
import os
import mimetypes
import SocketServer
from HTTPExceptions import HTTPException
from HTTPExceptions import HTTP400Error, HTTP404Error, HTTP405Error


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
    if ".." in request['URI']:
        raise HTTP400Error('Bad Request')
    if not request['URI'].startswith('/'):
    ##need to add something to check if this is an existing directory/filename
        raise HTTP400Error('Bad Request')


def check_request_protocol(request):
    if request['protocol'] != "HTTP/1.1":
        raise HTTP400Error('Bad Request')


def check_request_host(request):
    if 'host' not in request:
        raise HTTP400Error('Bad Request')


def resource_locator(uri):
    root = os.path.abspath(os.path.dirname(__file__))
    root = os.path.join(root, "webroot")
    dir_to_check = root + uri
    if not os.path.exists(dir_to_check):
        uri = ""
        return 'HTTP404Error'
    if os.path.isdir(dir_to_check):
        dir_contents = os.listdir(dir_to_check)
        return directory_formatter(dir_contents, uri)
    else:
        open_file = open(dir_to_check, 'r+')
        file_contents = open_file.read()
        return file_contents


def request_validator(request, content=""):
    try:
        check_request_method(request)
        check_request_URI(request)
        check_request_protocol(request)
        check_request_host(request)
        if content == 'HTTP404Error':
            return ('404', 'Resource Not Found', '<h1>404 - Resource Not Found</h1>')
        return ('200', 'OK', '{}'.format(content))
    except HTTPException as err:
        content = '<h1>{} - {}</h1>'.format(err.code, err.message)
        return (err.code, err.message, content)


def response_builder(response, content):
    mimetype = mimetypes.guess_type(content)[0]
    content_type = 'Content-Type: {}'.format(mimetype)
    template = '\r\n'.join(['HTTP/1.1 {} {}', content_type, '', '{}'])
    return template.format(*response)


def directory_formatter(content, dir_uri):
    output_list = "<html><ul>"
    for item in content:
        path = "{}/{}".format(dir_uri[1:], item)
        output_list += '<li><a href="{}">{}</a></li>'.format(path, item)
    output_list += "</ul></html>"
    return output_list


def echo(conn, addr):
    buffsize = 32
    print('Waiting for message...')
    while True:
        final_output = ''
        done = False
        while not done:
            msg_part = conn.recv(buffsize)
            final_output += msg_part
            if len(msg_part) < buffsize:
                done = True
        request = request_parser(final_output)
        content = resource_locator(request["URI"])
        response = request_validator(request, content)
        response = response_builder(response, request["URI"])
        conn.sendall(response)
        conn.close()
        break


def http_server():
    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SERVER_SOCKET.bind(('127.0.0.1', 50000))
    SERVER_SOCKET.listen(1)
    final_output = echo(SERVER_SOCKET.accept())
    SERVER_SOCKET.close()
    return final_output


if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server = StreamServer(('127.0.0.1', 50000), echo)
    print('Starting echo server on port 50000')
    server.serve_forever()
