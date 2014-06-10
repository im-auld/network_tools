import pytest
from echo_client import echo_client


def test_echo_client_and_server():
    our_test_val = "oiwejfojsoehfoihgioheiughirhgiehroghwoifwoeifjoiwej\
    foijweoifjowej918249294u293hiuhfowjeoifj"
    print our_test_val + "this was our print statement"
    assert echo_client(our_test_val) == our_test_val
