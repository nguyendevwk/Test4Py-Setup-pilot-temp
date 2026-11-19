import socket
import pytest
from tornado.netutil import add_accept_handler
from tornado.ioloop import IOLoop

def test_add_accept_handler_calls_callback(tmp_path):
    """The callback is invoked for each accepted connection."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(("127.0.0.1", 0))
    server.listen(5)

    received = []

    def cb(conn, addr):
        received.append((conn, addr))
        conn.close()

    remove = add_accept_handler(server, cb)

    # Create a client that connects to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server.getsockname())

    # Run the IOLoop until the callback is called
    loop = IOLoop.current()
    loop.add_timeout(loop.time() + 0.1, loop.stop)
    loop.start()

    assert len(received) == 1
    conn, addr = received[0]
    assert isinstance(conn, socket.socket)
    assert addr == client.getsockname()

    # Clean up
    client.close()
    server.close()
    remove()

def test_remove_handler_stops_accepting(tmp_path):
    """Removing the handler stops further connections from being accepted."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(("127.0.0.1", 0))
    server.listen(5)

    called = []

    def cb(conn, addr):
        called.append((conn, addr))
        conn.close()

    remove = add_accept_handler(server, cb)

    # First connection should be accepted
    client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client1.connect(server.getsockname())

    loop = IOLoop.current()
    loop.add_timeout(loop.time() + 0.1, loop.stop)
    loop.start()

    assert len(called) == 1

    # Remove the handler
    remove()

    # Second connection should not trigger the callback
    client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client2.connect(server.getsockname())

    loop.add_timeout(loop.time() + 0.1, loop.stop)
    loop.start()

    assert len(called) == 1  # still only one call

    # Clean up
    client1.close()
    client2.close()
    server.close()

def test_accept_handler_handles_blockingioerror(tmp_path):
    """The handler correctly stops when no more connections are pending."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(("127.0.0.1", 0))
    server.listen(1)

    called = []

    def cb(conn, addr):
        called.append((conn, addr))
        conn.close()

    remove = add_accept_handler(server, cb)

    # Connect a client to fill the backlog
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server.getsockname())

    loop = IOLoop.current()
    loop.add_timeout(loop.time() + 0.1, loop.stop)
    loop.start()

    # The callback should have been called once
    assert len(called) == 1

    # Now the socket has no pending connections; the next loop should
    # trigger a BlockingIOError and exit gracefully without raising.
    loop.add_timeout(loop.time() + 0.1, loop.stop)
    loop.start()

    # No additional calls should have been made
    assert len(called) == 1

    # Clean up
    client.close()
    server.close()
    remove()
