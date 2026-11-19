import socket
import ssl
import datetime
import pytest
from tornado.tcpclient import TCPClient
from tornado.ioloop import IOLoop
from tornado.netutil import Resolver
from tornado.gen import TimeoutError

# Helper to run a simple TCP echo server in a background thread
def start_echo_server(tmp_path):
    import threading
    import socketserver

    class EchoHandler(socketserver.BaseRequestHandler):
        def handle(self):
            data = self.request.recv(1024)
            if data:
                self.request.sendall(data)

    server = socketserver.TCPServer(("127.0.0.1", 0), EchoHandler)
    host, port = server.server_address

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, host, port, thread

def stop_echo_server(server):
    server.shutdown()
    server.server_close()

def test_tcpclient_connect_and_echo(tmp_path):
    """Normal connection: send data and receive echo."""
    server, host, port, thread = start_echo_server(tmp_path)
    try:
        client = TCPClient()
        stream = IOLoop.current().run_sync(
            lambda: client.connect(host, port, timeout=5)
        )
        # Send a message and read the echo
        message = b"hello"
        stream.write(message)
        received = stream.read_until_close()
        assert received == message
    finally:
        stop_echo_server(server)

def test_tcpclient_connect_timeout(tmp_path):
    """Connection attempt to an unreachable port should raise TimeoutError."""
    # Pick a port unlikely to be open
    host = "127.0.0.1"
    port = 65535  # usually closed
    client = TCPClient()
    with pytest.raises(TimeoutError):
        IOLoop.current().run_sync(
            lambda: client.connect(host, port, timeout=0.1)
        )

def test_tcpclient_source_ip_binding_error(tmp_path):
    """Binding to an invalid source IP should raise OSError."""
    server, host, port, thread = start_echo_server(tmp_path)
    try:
        client = TCPClient()
        # Use an IP that does not exist on the machine
        invalid_ip = "192.0.2.1"  # TEST-NET-1 reserved for documentation
        with pytest.raises(OSError):
            IOLoop.current().run_sync(
                lambda: client.connect(
                    host,
                    port,
                    source_ip=invalid_ip,
                    timeout=1,
                )
            )
    finally:
        stop_echo_server(server)
