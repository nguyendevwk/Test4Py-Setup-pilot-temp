import socket
import pytest
from tornado.netutil import bind_sockets

def test_bind_sockets_all_interfaces(tmp_path):
    # Bind to port 0 on all interfaces (empty string address)
    sockets = bind_sockets(0, address="")
    # Expect at least one socket (IPv4 or IPv6)
    assert sockets, "No sockets returned"
    for s in sockets:
        # Socket should be non-blocking and listening
        assert s.getblocking() is False
        assert s.getsockname()[1] != 0  # port assigned
        # Try to connect to the socket to ensure it is listening
        with socket.socket(s.family, socket.SOCK_STREAM) as client:
            client.settimeout(1)
            client.connect(s.getsockname())
            client.shutdown(socket.SHUT_RDWR)

def test_bind_sockets_reuse_port(tmp_path):
    # Bind two sockets on the same port with reuse_port enabled
    sockets1 = bind_sockets(0, reuse_port=True)
    port = sockets1[0].getsockname()[1]
    sockets2 = bind_sockets(port, reuse_port=True)
    # Both sockets should be listening on the same port
    assert sockets2[0].getsockname()[1] == port
    # Verify that both sockets can accept connections simultaneously
    with socket.socket(sockets1[0].family, socket.SOCK_STREAM) as client1, \
         socket.socket(sockets2[0].family, socket.SOCK_STREAM) as client2:
        client1.settimeout(1)
        client2.settimeout(1)
        client1.connect(sockets1[0].getsockname())
        client2.connect(sockets2[0].getsockname())
        client1.shutdown(socket.SHUT_RDWR)
        client2.shutdown(socket.SHUT_RDWR)

def test_bind_sockets_invalid_port():
    # Negative port numbers should raise OSError
    with pytest.raises(OSError):
        bind_sockets(-1)
