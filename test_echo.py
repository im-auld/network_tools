import pytest
from os import urandom
from echo_client import echo_client

tests = ["Hello", urandom(32), urandom(100), "exit"]


def test_echo_client_and_server():
    for test in tests:
        assert echo_client(test) == test
