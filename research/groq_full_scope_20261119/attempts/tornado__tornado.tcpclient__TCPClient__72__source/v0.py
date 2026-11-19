import asyncio
import socket
import ssl
import time
import datetime
import pytest
from tornado.tcpclient import TCPClient
from tornado.ioloop import IOLoop
from tornado.iostream import IOStream
from tornado.gen import TimeoutError

# Helper to run a simple echo server in a background thread
def start_echo_server(host="127.0.0.1", port=0):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(1)
    addr = srv.getsockname()
    async def handle_client():
        conn, _ = srv.accept()
        data = conn.recv(1024)
        conn.sendall(data)
        conn.close()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(handle_client())
    loop.run_forever()
    srv.close()

@pytest.mark.asyncio
async def test_tcpclient_connect_success(tmp_path):
    # Start echo server
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_sock.bind(("127.0.0.1", 0))
    srv_sock.listen(1)
    host, port = srv_sock.getsockname()
    async def echo():
        conn, _ = srv_sock.accept()
        data = conn.recv(1024)
        conn.sendall(data)
        conn.close()
    loop = asyncio.get_event_loop()
    loop.create_task(echo())
    client = TCPClient()
    stream = await client.connect(host, port)
    assert isinstance(stream, IOStream)
    msg = b"hello"
    await stream.write(msg)
    reply = await stream.read(len(msg))
    assert reply == msg
    stream.close()
    srv_sock.close()

@pytest.mark.asyncio
async def test_tcpclient_connect_timeout(tmp_path):
    # Resolve to an unreachable IP
    client = TCPClient()
    with pytest.raises(TimeoutError):
        await client.connect("10.255.255.1", 12345, timeout=0.1)

@pytest.mark.asyncio
async def test_tcpclient_source_ip_binding_error(tmp_path):
    # Attempt to bind to an invalid source IP
    client = TCPClient()
    with pytest.raises(OSError):
        await client.connect("127.0.0.1", 80, source_ip="256.256.256.256")
