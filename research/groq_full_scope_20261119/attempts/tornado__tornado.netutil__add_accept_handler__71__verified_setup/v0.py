import socket
import threading
import time

import pytest
from tornado.netutil import add_accept_handler
from tornado.ioloop import IOLoop


def _run_ioloop(loop, stop_after: float):
    """Run the IOLoop for a short period and then stop."""
    def stop():
        loop.stop()
    loop.add_timeout(loop.time() + stop_after, stop)
    loop.start()


def test_add_accept_handler_accepts_connection(tmp_path):
    """The callback is invoked with a new connection and its address."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 0))
    server.listen()
    server.setblocking(False)

    received = []

    def callback(conn, addr):
        received.append((conn, addr))
        conn.close()

    remove = add_accept_handler(server, callback)

    loop = IOLoop.current()
    thread = threading.Thread(target=_run_ioloop, args=(loop, 0.5))
    thread.start()

    # Connect a client to trigger the accept handler
    client = socket.create_connection(server.getsockname())
    client.close()

    thread.join()

    assert len(received) == 1
    conn, addr = received[0]
    assert isinstance(conn, socket.socket)
    assert addr == server.getsockname()
    remove()
    server.close()


def test_remove_handler_stops_accepting(tmp_path):
    """After the returned remover is called, no further connections are accepted."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 0))
    server.listen()
    server.setblocking(False)

    received = []

    def callback(conn, addr):
        received.append((conn, addr))
        conn.close()

    remove = add_accept_handler(server, callback)

    loop = IOLoop.current()
    thread = threading.Thread(target=_run_ioloop, args=(loop, 0.5))
    thread.start()

    # First connection should be accepted
    client1 = socket.create_connection(server.getsockname())
    client1.close()

    # Remove the handler before the second connection
    remove()

    # Second connection should not trigger the callback
    client2 = socket.create_connection(server.getsockname())
    client2.close()

    thread.join()

    assert len(received) == 1
    server.close()


def test_accept_handler_handles_nonblocking_and_aborted(tmp_path):
    """The handler correctly ignores BlockingIOError and ConnectionAbortedError."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 0))
    server.listen()
    server.setblocking(False)

    received = []

    def callback(conn, addr):
        received.append((conn, addr))
        conn.close()

    remove = add_accept_handler(server, callback)

    loop = IOLoop.current()
    thread = threading.Thread(target=_run_ioloop, args=(loop, 0.5))
    thread.start()

    # Simulate a connection that is immediately aborted by closing the client socket
    client = socket.create_connection(server.getsockname())
    client.close()  # abort before server accepts

    # Simulate a normal connection
    client2 = socket.create_connection(server.getsockname())
    client2.close()

    thread.join()

    # Only the normal connection should be recorded
    assert len(received) == 1
    conn, addr = received[0]
    assert isinstance(conn, socket.socket)
    assert addr == server.getsockname()
    remove()
    server.close()
