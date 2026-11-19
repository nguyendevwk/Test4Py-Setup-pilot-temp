import socket
import pytest
from tornado.netutil import bind_sockets


def test_bind_sockets_on_localhost_returns_listening_sockets():
    """Binding to localhost should return at least one listening socket."""
    sockets = bind_sockets(0, address="localhost")
    assert sockets, "No sockets returned for localhost"
    for s in sockets:
        # socket should be non-blocking and listening
        assert s.getblocking() is False
        # getsockname should contain a valid port
        host, port = s.getsockname()[:2]
        assert port != 0, "Socket bound to port 0 after binding"
        # try a quick connect to ensure it's listening
        with socket.socket(s.family, s.type) as c:
            c.settimeout(1)
            c.connect((host, port))
            # if connect succeeds, socket is listening
            assert True


def test_bind_sockets_with_port_zero_returns_same_port_for_all():
    """When port=0, all returned sockets should bind to the same dynamically allocated port."""
    sockets = bind_sockets(0, address="localhost")
    assert sockets, "No sockets returned for port 0"
    ports = {s.getsockname()[1] for s in sockets}
    assert len(ports) == 1, f"Different ports found: {ports}"
    # ensure the port is within the valid dynamic range
    port = ports.pop()
    assert 1024 <= port <= 65535, f"Port {port} out of expected range"


def test_bind_sockets_invalid_address_raises_error():
    """Binding to an invalid hostname should raise an exception."""
    with pytest.raises(OSError):
        bind_sockets(0, address="nonexistent.invalid.host.name")
