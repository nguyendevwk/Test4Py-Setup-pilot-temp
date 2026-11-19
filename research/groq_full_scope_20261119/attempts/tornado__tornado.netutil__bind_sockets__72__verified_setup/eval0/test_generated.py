import socket
import pytest
from tornado.netutil import bind_sockets


def test_bind_sockets_returns_same_port_for_zero_port(tmp_path):
    """When port is 0, all returned sockets should bind to the same allocated port."""
    sockets = bind_sockets(0, address="localhost")
    assert sockets, "No sockets were returned"
    # All sockets should have the same port number
    ports = {s.getsockname()[1] for s in sockets}
    assert len(ports) == 1, f"Expected a single port, got {ports}"
    # The port should be a positive integer
    port = ports.pop()
    assert 0 < port < 65536, f"Allocated port {port} is out of range"


def test_bind_sockets_reuse_port_raises_on_unsupported_platform():
    """If the platform does not support SO_REUSEPORT, a ValueError should be raised."""
    if not hasattr(socket, "SO_REUSEPORT"):
        with pytest.raises(ValueError, match="platform doesn't support SO_REUSEPORT"):
            bind_sockets(0, reuse_port=True)
    else:
        # On platforms that support SO_REUSEPORT, the call should succeed
        sockets = bind_sockets(0, reuse_port=True)
        assert sockets, "No sockets were returned when reuse_port is supported"


def test_bind_sockets_invalid_address_raises_oserror():
    """Binding to an invalid hostname should raise an OSError."""
    with pytest.raises(OSError):
        bind_sockets(0, address="nonexistent.invalid.host.name")
