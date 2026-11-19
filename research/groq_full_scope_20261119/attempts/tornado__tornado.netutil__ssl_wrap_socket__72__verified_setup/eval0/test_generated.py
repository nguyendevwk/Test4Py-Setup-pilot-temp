import socket
import ssl
import tempfile
import pathlib
import pytest
from tornado.netutil import ssl_wrap_socket, ssl_options_to_context


def test_ssl_wrap_socket_with_context_returns_sslsocket(tmp_path: pathlib.Path):
    """Wrapping a plain socket with a client SSLContext yields an SSLSocket."""
    # Create a pair of connected sockets
    sock1, sock2 = socket.socketpair()
    # Use a default client context (no certs needed)
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    # Wrap the client side socket
    wrapped = ssl_wrap_socket(sock1, ctx, server_hostname="example.com")
    assert isinstance(wrapped, ssl.SSLSocket)
    # The wrapped socket should be connected to the other end
    sock2.send(b"hello")
    data = wrapped.recv(5)
    assert data == b"hello"
    # Clean up
    wrapped.close()
    sock2.close()


def test_ssl_wrap_socket_with_dict_options(tmp_path: pathlib.Path):
    """ssl_options can be a dict that is converted to an SSLContext."""
    # Create a temporary self‑signed certificate file
    cert_file = tmp_path / "cert.pem"
    key_file = tmp_path / "key.pem"
    # Generate a simple self‑signed cert using openssl via subprocess
    # (allowed because it does not access the network or user files)
    import subprocess
    subprocess.check_call(
        [
            "openssl",
            "req",
            "-x509",
            "-nodes",
            "-newkey",
            "rsa:2048",
            "-keyout",
            str(key_file),
            "-out",
            str(cert_file),
            "-days",
            "1",
            "-subj",
            "/CN=localhost",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Prepare dict options
    options = {"certfile": str(cert_file), "keyfile": str(key_file), "ssl_version": ssl.PROTOCOL_TLS_SERVER}
    # Convert dict to context to ensure it works
    ctx = ssl_options_to_context(options, server_side=True)
    assert isinstance(ctx, ssl.SSLContext)
    # Create a pair of sockets
    sock1, sock2 = socket.socketpair()
    # Wrap the server side socket
    wrapped = ssl_wrap_socket(sock1, options, server_side=True)
    assert isinstance(wrapped, ssl.SSLSocket)
    # Verify that the socket is in server mode
    assert wrapped.server_side is True
    # Clean up
    wrapped.close()
    sock2.close()


def test_ssl_wrap_socket_invalid_options_raises_type_error():
    """Passing an unsupported type for ssl_options raises a TypeError."""
    sock1, sock2 = socket.socketpair()
    with pytest.raises(TypeError):
        ssl_wrap_socket(sock1, ssl_options=12345)  # invalid type
    sock1.close()
    sock2.close()
