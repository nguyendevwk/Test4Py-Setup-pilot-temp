import socket
import ssl
import pytest
from tornado.netutil import ssl_wrap_socket, ssl_options_to_context


def test_ssl_wrap_socket_returns_sslsocket(tmp_path):
    """Wrapping a plain socket with a default SSLContext should return an SSLSocket."""
    # Create a pair of connected sockets
    server_sock, client_sock = socket.socketpair()
    # Use a default SSLContext for client side
    context = ssl.create_default_context()
    # Wrap the client socket
    wrapped = ssl_wrap_socket(client_sock, context, server_hostname="example.com")
    assert isinstance(wrapped, ssl.SSLSocket)
    # The underlying socket should still be the same object
    assert wrapped.unwrap() is client_sock
    server_sock.close()
    client_sock.close()


def test_ssl_wrap_socket_server_side_with_certfile(tmp_path):
    """Server side wrapping with a certfile should succeed and set server_side flag."""
    # Generate a self‑signed certificate for testing
    cert_file = tmp_path / "cert.pem"
    key_file = tmp_path / "key.pem"
    # Use openssl via subprocess to create a self‑signed cert (available in test env)
    import subprocess
    subprocess.check_call(
        [
            "openssl",
            "req",
            "-x509",
            "-newkey",
            "rsa:2048",
            "-keyout",
            str(key_file),
            "-out",
            str(cert_file),
            "-days",
            "1",
            "-nodes",
            "-subj",
            "/CN=localhost",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Build ssl_options dict
    ssl_opts = {
        "certfile": str(cert_file),
        "keyfile": str(key_file),
        "ssl_version": ssl.PROTOCOL_TLS_SERVER,
    }
    # Create a pair of connected sockets
    server_sock, client_sock = socket.socketpair()
    # Wrap the server socket
    wrapped = ssl_wrap_socket(server_sock, ssl_opts, server_side=True)
    assert isinstance(wrapped, ssl.SSLSocket)
    # The wrapped socket should be in server mode
    assert wrapped.server_side is True
    server_sock.close()
    client_sock.close()


def test_ssl_options_to_context_invalid_keyword_raises():
    """Passing an unknown keyword to ssl_options_to_context should raise an AssertionError."""
    invalid_opts = {"unknown_key": "value"}
    with pytest.raises(AssertionError):
        ssl_options_to_context(invalid_opts)
