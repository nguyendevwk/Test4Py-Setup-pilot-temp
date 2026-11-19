import socket
import pytest
from tornado.netutil import add_accept_handler
from tornado.ioloop import IOLoop

def test_add_accept_handler_calls_callback(tmp_path):
    """The callback is invoked for each accepted connection."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(("127.0.0.1", 0))
    server.listen(1)

    received = []

    def cb(conn, addr):
        received.append((conn, addr))
        conn.close()

    remove = add_accept_handler(server, cb)

    # Connect a client
    client = socket.create_connection(server.getsockname())
    client.close()

    # Run the IOLoop until the callback has been called
    loop = IOLoop.current()
    loop.add_timeout(loop.time() + 0.1, loop.stop)
    loop.start()

    assert len(received) == 1
    conn, addr = received[0]
    assert isinstance(conn, socket.socket)
    assert addr == server.getsockname()

    remove()
    server.close()

def test_remove_handler_stops_accepting(tmp_path):
    """Removing the handler prevents further connections from being accepted."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(("127.0.0.1", 0))
    server.listen(1)

    calls = []

    def cb(conn, addr):
        calls.append((conn, addr))
        conn.close()

    remove = add_accept_handler(server, cb)

    # Accept one connection
    client1 = socket.create_connection(server.getsockname())
    client1.close()

    loop = IOLoop.current()
    loop.add_timeout(loop.time() + 0.1, loop.stop)
    loop.start()

    assert len(calls) == 1

    # Remove the handler
    remove()

    # Attempt to accept another connection
    client2 = socket.create_connection(server.getsockname())
    client2.close()

    loop.add_timeout(loop.time() + 0.1, loop.stop)
    loop.start()

    # No new callback should have been invoked
    assert len(calls) == 1

    server.close()

def test_accept_handler_handles_nonblocking(tmp_path):
    """The handler correctly handles BlockingIOError when no connections are pending."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(("127.0.0.1", 0))
    server.listen(1)

    called = False

    def cb(conn, addr):
        nonlocal called
        called = True
        conn.close()

    remove = add_accept_handler(server, cb)

    # Run the IOLoop for a short time without any pending connections
    loop = IOLoop.current()
    loop.add_timeout(loop.time() + 0.1, loop.stop)
    loop.start()

    # Callback should not have been called
    assert not called

    remove()
    server.close()
