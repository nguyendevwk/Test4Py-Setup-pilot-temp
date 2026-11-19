import socket
import ssl
import datetime
import pytest
from tornado.tcpclient import TCPClient
from tornado.ioloop import IOLoop
from tornado.gen import TimeoutError
from tornado.netutil import Resolver


def _start_echo_server(host: str, port: int):
    """Start a simple blocking echo server in a background thread."""
    import threading

    def server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen()
            conn, _ = s.accept()
            with conn:
                data = conn.recv(1024)
                conn.sendall(data)

    t = threading.Thread(target=server, daemon=True)
    t.start()
    return t


def test_tcpclient_connect_success(tmp_path):
    """TCPClient should connect to a local echo server and return a stream."""
    host = "127.0.0.1"
    port = 0  # let OS pick a free port
    # Find a free port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        port = s.getsockname()[1]
    server_thread = _start_echo_server(host, port)

    client = TCPClient()
    stream = IOLoop.current().run_sync(
        lambda: client.connect(host, port, timeout=5)
    )
    assert stream is not None
    stream.write(b"hello")
    data = stream.read_until_close()
    assert data == b"hello"
    stream.close()
    client.close()


def test_tcpclient_connect_timeout(tmp_path):
    """TCPClient should raise TimeoutError when the host is unreachable."""
    host = "10.255.255.1"  # non-routable IP
    port = 12345
    client = TCPClient()
    with pytest.raises(TimeoutError):
        IOLoop.current().run_sync(
            lambda: client.connect(host, port, timeout=1)
        )
    client.close()


def test_tcpclient_source_ip_binding_error(tmp_path):
    """TCPClient should raise OSError when binding to an invalid source IP."""
    host = "127.0.0.1"
    port = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        port = s.getsockname()[1]
    server_thread = _start_echo_server(host, port)

    client = TCPClient()
    # Use an invalid source IP that cannot be bound
    with pytest.raises(OSError):
        IOLoop.current().run_sync(
            lambda: client.connect(
                host,
                port,
                source_ip="256.256.256.256",
                timeout=5,
            )
        )
    client.close()
