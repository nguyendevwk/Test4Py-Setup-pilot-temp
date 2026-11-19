import socket
import pytest
from tornado.netutil import bind_sockets

def test_bind_sockets_auto_port(tmp_path):
    """Binding to port 0 should allocate a free port and return a listening socket."""
    sockets = bind_sockets(0, address="localhost")
    assert len(sockets) >= 1
    sock = sockets[0]
    assert sock.fileno() != -1
    host, port = sock.getsockname()
    assert port != 0
    # The socket should be listening; a connect attempt should succeed.
    with socket.create_connection(("localhost", port), timeout=1) as conn:
        assert conn is not None

def test_bind_sockets_reuse_port_unsupported():
    """If the platform does not support SO_REUSEPORT, a ValueError should be raised."""
    # Temporarily remove SO_REUSEPORT if it exists.
    has_attr = hasattr(socket, "SO_REUSEPORT")
    original = getattr(socket, "SO_REUSEPORT", None)
    try:
        if has_attr:
            delattr(socket, "SO_REUSEPORT")
        with pytest.raises(ValueError, match="SO_REUSEPORT"):
            bind_sockets(0, address="localhost", reuse_port=True)
    finally:
        if has_attr:
            setattr(socket, "SO_REUSEPORT", original)

def test_bind_sockets_invalid_address():
    """Providing an invalid hostname should raise a socket.gaierror."""
    with pytest.raises(socket.gaierror):
        bind_sockets(0, address="this-host-does-not-exist-xyz")
