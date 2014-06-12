import pytest
from http_server import http_server, request_parser, request_validator, response_builder
from echo_client import echo_client

request_200 = """GET / HTTP/1.1\r\nHost: 127.0.0.1:50000
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:29.0) Gecko/20100101 Firefox/29.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Cache-Control: max-age=0"""


request_400 = """GET / HP/1.1\r\nHost: 127.0.0.1:50000
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:29.0) Gecko/20100101 Firefox/29.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Cache-Control: max-age=0"""

request_405 = """POST / HP/1.1\r\nHost: 127.0.0.1:50000
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:29.0) Gecko/20100101 Firefox/29.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Cache-Control: max-age=0"""

def test_request_parser():
    request = request_parser(request_200)
    print(request)
    assert request['method'] == 'GET'
    assert request['URI'] == '/'
    assert request['protocol'] == 'HTTP/1.1'
    assert request['host'] == '127.0.0.1:50000'
    
def test_200_response():
    request = request_parser(request_200)
    response = request_validator(request)
    assert response[0] == '200'
    assert response[1] == 'OK'
    assert response[2] == 'This is a message'
    
def test_400_response():
    request = request_parser(request_400)
    response = request_validator(request)
    assert response[0] == '400'
    assert response[1] == 'Bad Request'
    assert response[2] == '<h1>400 - Bad Request</h1>'
    
def test_405_response():
    request = request_parser(request_405)
    response = request_validator(request)
    assert response[0] == '405'
    assert response[1] == 'Method Not Allowed'
    assert response[2] == '<h1>405 - Method Not Allowed</h1>'
    
def test_response_builder():
    request = request_parser(request_200)
    response = request_validator(request)
    response = response_builder(response)
    assert response == 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nThis is a message'
    
    
    
    
    
    
    
    
    
    