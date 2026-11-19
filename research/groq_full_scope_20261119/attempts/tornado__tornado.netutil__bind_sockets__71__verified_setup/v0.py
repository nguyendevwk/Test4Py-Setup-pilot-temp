import socket
import pytest
from tornado.netutil import bind_sockets


def test_bind_sockets_auto_port_and_ipv6_consistency(tmp_path):
    """When port is 0, all returned sockets should bind to the same port."""
    sockets = bind_sockets(0, address=None, family=socket.AF_UNSPEC, backlog=1)
    assert sockets, "No sockets were returned"
    # All sockets should have the same port number
    ports = {s.getsockname()[1] for s in sockets}
    assert len(ports) == 1, f"Different ports found: {ports}"
    # Ensure sockets are listening
    for s in sockets:
        assert s.getsockname()[1] == ports.pop()
        assert s.getsockname()[0] in ("0.0.0.0", "::") or s.getsockname()[0] == ""


def test_bind_sockets_reuse_port_unsupported():
    """If the platform does not support SO_REUSEPORT, a ValueError is raised."""
    if hasattr(socket, "SO_REUSEPORT"):
        pytest.skip("Platform supports SO_REUSEPORT; cannot test unsupported case")
    with pytest.raises(ValueError, match="doesn't support SO_REUSEPORT"):
        bind_sockets(0, reuse_port=True)


def test_bind_sockets_invalid_address_raises():
    """Providing an invalid hostname should raise an OSError."""
    with pytest.raises(OSError):
        bind_sockets(0, address="this-hostname-should-not-exist", family=socket.AF_UNSPEC)
