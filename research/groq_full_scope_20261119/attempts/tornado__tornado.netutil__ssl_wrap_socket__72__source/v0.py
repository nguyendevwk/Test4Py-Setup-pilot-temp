import socket
import ssl
import pytest
from tornado.netutil import ssl_wrap_socket


def test_ssl_wrap_socket_returns_sslsocket_and_passes_hostname(tmp_path):
    """Wrapping a plain socket with a default SSL context returns an SSLSocket
    and the server_hostname argument is forwarded correctly."""
    # Create a pair of connected sockets
    sock1, sock2 = socket.socketpair()
    try:
        # Use a default client context
        context = ssl.create_default_context()
        # Wrap the client side socket
        wrapped = ssl_wrap_socket(sock1, context, server_hostname="example.com")
        # The returned object must be an SSLSocket
        assert isinstance(wrapped, ssl.SSLSocket)
        # The underlying socket should still be the same
        assert wrapped.getsockname() == sock1.getsockname()
        # The server_hostname should be stored in the SSLObject
        assert wrapped.server_hostname == "example.com"
    finally:
        sock1.close()
        sock2.close()


def test_ssl_wrap_socket_accepts_dict_options_and_server_side(tmp_path):
    """ssl_wrap_socket accepts a dictionary of SSL options and correctly
    sets server_side when provided."""
    # Create a pair of connected sockets
    sock1, sock2 = socket.socketpair()
    try:
        # Prepare SSL options dictionary
        ssl_opts = {
            "certfile": str(tmp_path / "cert.pem"),
            "keyfile": str(tmp_path / "key.pem"),
        }
        # Create a self‑signed cert for testing
        # (openssl is not available, so we skip actual cert generation;
        # the test only verifies that the function accepts the dict)
        # Wrap the server side socket
        wrapped = ssl_wrap_socket(sock1, ssl_opts, server_side=True)
        assert isinstance(wrapped, ssl.SSLSocket)
        # server_side should be True
        assert wrapped.server_side is True
    finally:
        sock1.close()
        sock2.close()


def test_ssl_wrap_socket_invalid_ssl_options_raises_type_error():
    """Passing an unsupported type for ssl_options raises a TypeError."""
    sock = socket.socket()
    with pytest.raises(TypeError):
        ssl_wrap_socket(sock, ssl_options=12345)  # invalid type
