import socket
import time
import threading

import pytest
from tornado.ioloop import IOLoop
from tornado.netutil import add_accept_handler


def _run_loop(loop, stop_after: float):
    """Run the given IOLoop for a short time and then stop it."""
    def stop():
        loop.stop()
    loop.add_timeout(loop.time() + stop_after, stop)
    loop.start()


def test_add_accept_handler_accepts_connection(tmp_path):
    """The callback is invoked with a new connection and its address."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(("127.0.0.1", 0))
    server.listen(1)

    received = []

    def callback(conn, addr):
        received.append((conn, addr))
        conn.close()

    remove = add_accept_handler(server, callback)

    loop = IOLoop.current()
    thread = threading.Thread(target=_run_loop, args=(loop, 0.5))
    thread.start()

    # Connect a client to trigger the accept handler
    client = socket.create_connection(server.getsockname())
    client.close()

    thread.join()
    remove()
    server.close()

    assert len(received) == 1
    conn, addr = received[0]
    assert isinstance(conn, socket.socket)
    assert addr == server.getsockname()


def test_add_accept_handler_removal(tmp_path):
    """Removing the handler stops further callbacks."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(("127.0.0.1", 0))
    server.listen(1)

    call_count = 0

    def callback(conn, addr):
        nonlocal call_count
        call_count += 1
        conn.close()

    remove = add_accept_handler(server, callback)

    loop = IOLoop.current()
    thread = threading.Thread(target=_run_loop, args=(loop, 0.5))
    thread.start()

    # First connection should be accepted
    client1 = socket.create_connection(server.getsockname())
    client1.close()

    # Remove handler before second connection
    remove()

    # Second connection should not trigger callback
    client2 = socket.create_connection(server.getsockname())
    client2.close()

    thread.join()
    server.close()

    assert call_count == 1


def test_add_accept_handler_no_connection(tmp_path):
    """If no connections arrive, the callback is never called and no exception occurs."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(("127.0.0.1", 0))
    server.listen(1)

    called = False

    def callback(conn, addr):
        nonlocal called
        called = True
        conn.close()

    remove = add_accept_handler(server, callback)

    loop = IOLoop.current()
    thread = threading.Thread(target=_run_loop, args=(loop, 0.5))
    thread.start()

    # Do not connect any client
    thread.join()
    remove()
    server.close()

    assert not called
