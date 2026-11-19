import socket
import time
import pytest
from tornado.netutil import add_accept_handler
from tornado.ioloop import IOLoop

def _start_loop_and_stop(loop, timeout=0.1):
    """Start the IOLoop and stop it after `timeout` seconds."""
    loop.add_timeout(time.time() + timeout, loop.stop)
    loop.start()

def _create_server_socket(tmp_path):
    """Create a non‑blocking TCP server socket bound to an OS‑assigned port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.bind(("127.0.0.1", 0))
    sock.listen()
    return sock

def _connect_client(port):
    """Connect a client socket to the given port."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", port))
    return client

def test_add_accept_handler_normal(tmp_path):
    """Verify that a single connection triggers the callback."""
    server = _create_server_socket(tmp_path)
    received = []

    def callback(conn, addr):
        received.append((conn, addr))
        conn.close()

    remove = add_accept_handler(server, callback)

    client = _connect_client(server.getsockname()[1])

    loop = IOLoop.current()
    _start_loop_and_stop(loop)

    assert len(received) == 1
    conn, addr = received[0]
    assert isinstance(conn, socket.socket)
    assert addr[0] == "127.0.0.1"
    client.close()
    remove()
    server.close()

def test_add_accept_handler_removal(tmp_path):
    """Verify that removing the handler stops further callbacks."""
    server = _create_server_socket(tmp_path)
    received = []

    def callback(conn, addr):
        received.append((conn, addr))
        conn.close()

    remove = add_accept_handler(server, callback)
    remove()  # remove before any connection

    client = _connect_client(server.getsockname()[1])

    loop = IOLoop.current()
    _start_loop_and_stop(loop)

    assert len(received) == 0
    client.close()
    server.close()

def test_add_accept_handler_multiple_connections(tmp_path):
    """Verify that multiple connections are accepted up to the backlog."""
    server = _create_server_socket(tmp_path)
    received = []

    def callback(conn, addr):
        received.append((conn, addr))
        conn.close()

    add_accept_handler(server, callback)

    # Create several clients in quick succession
    clients = [_connect_client(server.getsockname()[1]) for _ in range(5)]

    loop = IOLoop.current()
    _start_loop_and_stop(loop)

    assert len(received) == 5
    for conn, addr in received:
        assert isinstance(conn, socket.socket)
        assert addr[0] == "127.0.0.1"

    for c in clients:
        c.close()
    server.close()
