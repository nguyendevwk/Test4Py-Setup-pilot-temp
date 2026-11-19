import socket
import ssl
import pytest
from tornado.netutil import ssl_wrap_socket, ssl_options_to_context

def test_ssl_wrap_socket_with_context(tmp_path):
    # Create a pair of connected sockets
    s1, s2 = socket.socketpair()
    # Use a default SSL context
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    # Wrap the client side socket
    wrapped = ssl_wrap_socket(s1, ctx, server_hostname="localhost")
    assert isinstance(wrapped, ssl.SSLSocket)
    # The underlying socket should be the same as the original
    assert wrapped.getsockname() == s1.getsockname()
    # The wrapped socket should be in non-blocking mode
    assert wrapped.getblocking() is False
    # Clean up
    wrapped.close()
    s2.close()

def test_ssl_wrap_socket_server_side_default(tmp_path):
    # Create a pair of connected sockets
    s1, s2 = socket.socketpair()
    # Use a default SSL context
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # Wrap the server side socket without specifying server_side
    wrapped = ssl_wrap_socket(s1, ctx, server_hostname="localhost")
    # server_side should default to False, but the context is for client auth
    # The wrapped socket should still be an SSLSocket
    assert isinstance(wrapped, ssl.SSLSocket)
    # The wrapped socket should be in non-blocking mode
    assert wrapped.getblocking() is False
    # Clean up
    wrapped.close()
    s2.close()

def test_ssl_wrap_socket_invalid_options_raises():
    # Provide a dict with an invalid keyword
    invalid_options = {"invalid_key": "value"}
    s = socket.socket()
    with pytest.raises(AssertionError):
        ssl_options_to_context(invalid_options)
    # Ensure that ssl_wrap_socket propagates the error when given invalid dict
    with pytest.raises(AssertionError):
        ssl_wrap_socket(s, invalid_options)
