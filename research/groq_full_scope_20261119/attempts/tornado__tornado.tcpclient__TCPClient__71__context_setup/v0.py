import socket
import time
import datetime
import ssl
import pytest
from tornado.tcpclient import TCPClient
from tornado.iostream import IOStream
from tornado.ioloop import IOLoop
from tornado.gen import TimeoutError

@pytest.mark.asyncio
async def test_connect_success(tmp_path):
    """TCPClient should successfully connect to a local echo server."""
    # Start a simple echo server on an available port
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("127.0.0.1", 0))
    server_sock.listen(1)
    host, port = server_sock.getsockname()

    async def server_loop():
        conn, _ = server_sock.accept()
        with conn:
            data = conn.recv(1024)
            conn.sendall(data)

    # Run the server in a background thread
    loop = IOLoop.current()
    server_future = loop.run_in_executor(None, server_loop)

    client = TCPClient()
    stream = await client.connect(host, port, timeout=5)
    assert isinstance(stream, IOStream)

    test_msg = b"hello"
    stream.write(test_msg)
    await stream.read_bytes(len(test_msg))
    # The server echoes back the same data
    stream.close()
    server_sock.close()
    await server_future

@pytest.mark.asyncio
async def test_connect_timeout(tmp_path):
    """TCPClient should raise TimeoutError when the connection times out."""
    # Use an IP that is unlikely to be reachable
    unreachable_host = "10.255.255.1"
    port = 12345
    client = TCPClient()
    with pytest.raises(TimeoutError):
        await client.connect(unreachable_host, port, timeout=0.1)

@pytest.mark.asyncio
async def test_source_ip_binding_error(tmp_path):
    """TCPClient should raise OSError when binding to an invalid source IP."""
    # Start a dummy server to accept connections
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("127.0.0.1", 0))
    server_sock.listen(1)
    host, port = server_sock.getsockname()

    async def server_loop():
        conn, _ = server_sock.accept()
        with conn:
            conn.recv(1024)

    loop = IOLoop.current()
    server_future = loop.run_in_executor(None, server_loop)

    client = TCPClient()
    # Use an invalid source IP that cannot be bound
    with pytest.raises(OSError):
        await client.connect(host, port, source_ip="256.256.256.256", timeout=5)

    server_sock.close()
    await server_future
