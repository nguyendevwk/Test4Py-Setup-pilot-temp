import socket
import ssl
import datetime
import pytest
from tornado.tcpclient import TCPClient
from tornado.ioloop import IOLoop
from tornado.gen import TimeoutError

@pytest.fixture
def free_port():
    """Return an unused TCP port by binding to port 0."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    addr, port = s.getsockname()
    s.close()
    return port

def _start_echo_server(port):
    """Start a simple echo server in a background thread."""
    import threading
    def server():
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.01", port))
        srv.listen(1)
        conn, _ = srv.accept()
        data = conn.recv(1024)
        conn.sendall(data)
        conn.close()
        srv.close()
    t = threading.Thread(target=server, daemon=True)
    t.start()
    return t

def test_tcpclient_connect_success(free_port):
    """TCPClient should successfully connect to a local echo server."""
    server_thread = _start_echo_server(free_port)
    client = TCPClient()
    loop = IOLoop.current()
    stream = loop.run_sync(lambda: client.connect("127.0.0.1", free_port))
    # Send and receive data to verify the stream works
    loop.run_sync(lambda: stream.write(b"hello"))
    data = loop.run_sync(lambda: stream.read_bytes(5))
    assert data == b"hello"
    stream.close()
    client.close()
    server_thread.join(timeout=1)

def test_tcpclient_connect_timeout(free_port):
    """TCPClient should raise TimeoutError when connection times out."""
    # Use a port that is not listening to trigger timeout
    client = TCPClient()
    loop = IOLoop.current()
    with pytest.raises(TimeoutError):
        loop.run_sync(lambda: client.connect("127.0.0.1", free_port, timeout=0.001))
    client.close()

def test_tcpclient_invalid_timeout():
    """Passing an unsupported timeout type should raise TypeError."""
    client = TCPClient()
    loop = IOLoop.current()
    with pytest.raises(TypeError):
        loop.run_sync(lambda: client.connect("127.0.0.1", 80, timeout="invalid"))
    client.close()
