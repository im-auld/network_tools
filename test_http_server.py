import pytest
from http_server import http_server
from echo_client import echo_client


tests = {"GET / HTTP/1.1 Host: 127.0.0.1:50000 Connection: keep-alive Cache-Control: max-age=0":
        "200 OK: Your URI is /",
        "POST / HTTP/1.1 Host: 127.0.0.1:50000 Connection: keep-alive Cache-Control: max-age=0":
        "405 Method Not Allowed",
        "GET HTTP/1.1 Host: 127.0.0.1:50000 Connection: keep-alive Cache-Control: max-age=0":
        "404 Not Found",
        "GET / HTTP/1.0 Host: 127.0.0.1:50000 Connection: keep-alive Cache-Control: max-age=0":
        "400 Bad Request",
        "GET / HTTP/1.1 Connection: keep-alive Cache-Control: max-age=0":
        "404 Not Found",
        "GET / ":
        "400 Bad Request"}

def test_http_server():
    for test in tests:
        print test
        assert echo_client(test) == tests[test]
