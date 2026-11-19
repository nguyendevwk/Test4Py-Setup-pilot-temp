import pytest
import threading
import http.server
import socket
import os
from tornado.httpclient import HTTPClient, HTTPError, HTTPResponse
from tornado.ioloop import IOLoop
from tornado import gen

# Helper to start a simple HTTP server in a background thread
def start_test_server(tmp_path):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # suppress logging

    port = 0  # let OS pick a free port
    server = http.server.HTTPServer(Handler, bind_address=('127.0.0.1', port))
    addr, port = server.server_address
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, addr, port, thread

@pytest.fixture
def http_server(tmp_path):
    server, addr, port, thread = start_test_server(tmp_path)
    yield addr, port
    server.shutdown()
    thread.join()

def test_fetch_returns_response_with_body(http_server, tmp_path):
    addr, port = http_server
    # Create a test file
    content = b"Hello, world!"
    file_path = tmp_path / "test.txt"
    file_path.write_bytes(content)

    # The server serves files from tmp_path
    os.chdir(tmp_path)

    client = HTTPClient()
    url = f"http://{addr}:{port}/test.txt"
    response = client.fetch(url)
    assert isinstance(response, HTTPResponse)
    assert response.code == 200
    assert response.body == content
    client.close()

def test_close_releases_resources():
    client = HTTPClient()
    # After close, attempting to fetch should raise an exception
    client.close()
    with pytest.raises(RuntimeError):
        client.fetch("http://example.com/")

def test_fetch_invalid_domain_raises_http_error():
    client = HTTPClient()
    with pytest.raises(HTTPError) as excinfo:
        client.fetch("http://nonexistent.invalid/")
    assert excinfo.value.response is None
    client.close()
