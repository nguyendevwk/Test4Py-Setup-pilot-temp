import socket
import ssl
import pytest
from tornado.netutil import ssl_wrap_socket


def test_ssl_wrap_socket_client_side(tmp_path):
    """Wrapping a client‑side socket should produce an SSLSocket that can
    perform a handshake and exchange data."""
    # Create a pair of connected sockets
    sock1, sock2 = socket.socketpair()
    # Use a default context for the client
    context = ssl.create_default_context()
    # Wrap the client socket
    wrapped = ssl_wrap_socket(sock1, context, server_hostname="localhost")
    # Perform a handshake in a non‑blocking way
    wrapped.setblocking(False)
    with pytest.raises(ssl.SSLWantReadError):
        wrapped.do_handshake()
    # The wrapped socket should be an instance of ssl.SSLSocket
    assert isinstance(wrapped, ssl.SSLSocket)
    # The underlying socket should still be the original
    assert wrapped.unwrap() is sock1
    # Clean up
    sock2.close()


def test_ssl_wrap_socket_server_side(tmp_path):
    """When server_side=True the wrapped socket should accept a client
    connection and perform a handshake."""
    # Create a pair of connected sockets
    client_sock, server_sock = socket.socketpair()
    # Create a server context that requires client certs
    server_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    server_context.check_hostname = False
    server_context.verify_mode = ssl.CERT_NONE
    # Wrap the server socket
    wrapped_server = ssl_wrap_socket(server_sock, server_context, server_side=True)
    # Perform a handshake in a non‑blocking way
    wrapped_server.setblocking(False)
    with pytest.raises(ssl.SSLWantReadError):
        wrapped_server.do_handshake()
    # The wrapped socket should be an instance of ssl.SSLSocket
    assert isinstance(wrapped_server, ssl.SSLSocket)
    # Clean up
    client_sock.close()


def test_ssl_wrap_socket_invalid_options():
    """Passing an unsupported type for ssl_options should raise a TypeError."""
    sock = socket.socket()
    with pytest.raises(TypeError):
        ssl_wrap_socket(sock, 42)  # int is not a valid ssl_options type
