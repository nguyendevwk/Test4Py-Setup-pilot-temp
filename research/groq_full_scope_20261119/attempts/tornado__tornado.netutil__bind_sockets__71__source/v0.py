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
    # Ensure sockets are listening (non-zero backlog)
    for s in sockets:
        assert s.getsockname()[1] == ports.pop()
        # Try to connect to the socket to confirm it is listening
        with socket.create_connection(s.getsockname(), timeout=1):
            pass
    # Clean up
    for s in sockets:
        s.close()


def test_bind_sockets_reuse_port_unsupported():
    """If the platform does not support SO_REUSEPORT, ValueError is raised."""
    if hasattr(socket, "SO_REUSEPORT"):
        pytest.skip("Platform supports SO_REUSEPORT; test not applicable")
    with pytest.raises(ValueError, match="platform doesn't support SO_REUSEPORT"):
        bind_sockets(0, reuse_port=True)


def test_bind_sockets_invalid_address_raises():
    """Providing an invalid hostname should raise OSError."""
    with pytest.raises(OSError):
        bind_sockets(0, address="this_host_does_not_exist_12345")
