import socket
import pytest
from tornado.netutil import add_accept_handler
from tornado.ioloop import IOLoop

def test_add_accept_handler_accepts_connection(tmp_path):
    """The handler should accept a connection and invoke the callback."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 0))
    server.listen()
    server.setblocking(False)

    received = []

    def cb(conn, addr):
        received.append((conn, addr))
        conn.close()

    remove = add_accept_handler(server, cb)

    # Connect a client
    client = socket.create_connection(server.getsockname())
    client.close()

    # Run the IOLoop until the callback is called
    loop = IOLoop.current()
    loop.add_timeout(loop.time() + 0.1, loop.stop)
    loop.start()

    assert len(received) == 1
    conn, addr = received[0]
    assert isinstance(conn, socket.socket)
    assert addr == server.getsockname()

    # Removing the handler stops further callbacks
    remove()
    client2 = socket.create_connection(server.getsockname())
    client2.close()
    loop.add_timeout(loop.time() + 0.1, loop.stop)
    loop.start()
    assert len(received) == 1  # no new callback

    server.close()


def test_add_accept_handler_backlog_limit(tmp_path):
    """The handler should accept up to _DEFAULT_BACKLOG connections."""
    from tornado.netutil import _DEFAULT_BACKLOG

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 0))
    server.listen(_DEFAULT_BACKLOG)
    server.setblocking(False)

    received = []

    def cb(conn, addr):
        received.append((conn, addr))
        conn.close()

    add_accept_handler(server, cb)

    # Open many clients, more than the backlog
    clients = []
    for _ in range(_DEFAULT_BACKLOG + 5):
        try:
            c = socket.create_connection(server.getsockname())
            clients.append(c)
        except OSError:
            # Some OS may refuse more than backlog connections
            break

    loop = IOLoop.current()
    loop.add_timeout(loop.time() + 0.1, loop.stop)
    loop.start()

    # The number of callbacks should not exceed the backlog
    assert len(received) <= _DEFAULT_BACKLOG
    for conn, _ in received:
        conn.close()
    for c in clients:
        c.close()
    server.close()


def test_add_accept_handler_handles_blockingioerror(tmp_path):
    """When no connections are pending, the handler should exit gracefully."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 0))
    server.listen()
    server.setblocking(False)

    called = False

    def cb(conn, addr):
        nonlocal called
        called = True
        conn.close()

    add_accept_handler(server, cb)

    loop = IOLoop.current()
    loop.add_timeout(loop.time() + 0.1, loop.stop)
    loop.start()

    assert not called  # no connection, callback should not run
    server.close()
