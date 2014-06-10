import pytest
from os import urandom
from subprocess import call
from echo_client import echo_client
from echo_server import echo_server

tests = ['Hello, world', u'Hello, world', urandom(32)]

def test_echo_server():
    for test in tests:
        assert echo_client(test) == test
    echo_client('^D')