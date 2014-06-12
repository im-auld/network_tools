import socket
import os
import mimetypes
import pdb
from HTTPExceptions import HTTPException, HTTP400Error, HTTP404Error, HTTP405Error


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
    if os.path.isdir(dir_to_check):
        dir_contents = os.listdir(dir_to_check)
        return directory_formatter(dir_contents)
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
        return ('200', 'OK', '{}'.format(content))
    except HTTPException as err:
        return (err.code, err.message, '<h1>{} - {}</h1>'.format(err.code, err.message))


def response_builder(response, content):
    mimetype = mimetypes.guess_type(content)[0]
    content_type = 'Content-Type: {}'.format(mimetype)
    template = '\r\n'.join(['HTTP/1.1 {} {}', content_type, '', '{}'])
    return template.format(*response)


def directory_formatter(content):
    output_list = "<ul>"
    for item in content:
        output_list += "<li>{}</li>".format(item)
    output_list += "</ul>"
    return output_list


def file_formatter(content):
    file_format = mimetypes.guess_type(content)[0]
    #if file_format.split("/")[0] == "image":
    #    '<img src="{file_name}" alt="{file_name}">'.format(file_name=content)
    #else:
    #    return "<body> 'I am a random placeholder' </body>"


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
        content = resource_locator(request["URI"])
        response = request_validator(request, content)
        response = response_builder(response, request["URI"])
        conn.sendall(response)
        conn.close()
    SERVER_SOCKET.close()
    return final_output


if __name__ == '__main__':
    http_server()
