import asyncio
import pytest
from tornado import httpserver, web, ioloop, httpclient, httputil
from tornado.testing import AsyncTestCase, gen_test
from tornado.ioloop import IOLoop

# Helper to start a simple HTTP server in a background thread
def start_test_server(handler_class, port=0):
    app = web.Application([(r"/", handler_class)])
    server = httpserver.HTTPServer(app)
    server.listen(port)
    return server, server._port

class SimpleHandler(web.RequestHandler):
    def get(self):
        self.write("Hello, world!")

class NotFoundHandler(web.RequestHandler):
    def get(self):
        self.set_status(404)
        self.write("Not found")

class DelayedHandler(web.RequestHandler):
    async def get(self):
        await asyncio.sleep(0.1)
        self.write("Delayed response")

@pytest.mark.asyncio
async def test_successful_fetch(tmp_path):
    """HTTPClient should return a response with expected body for a 200 OK."""
    server, port = start_test_server(SimpleHandler)
    client = httpclient.HTTPClient()
    try:
        url = f"http://127.0.0.1:{port}/"
        response = client.fetch(url)
        assert response.code == 200
        assert response.body == b"Hello, world!"
        assert isinstance(response, httpclient.HTTPResponse)
    finally:
        client.close()
        server.stop()

@pytest.mark.asyncio
async def test_404_error(tmp_path):
    """HTTPClient should raise HTTPError with code 404 and provide response."""
    server, port = start_test_server(NotFoundHandler)
    client = httpclient.HTTPClient()
    try:
        url = f"http://127.0.0.1:{port}/"
        with pytest.raises(httpclient.HTTPError) as excinfo:
            client.fetch(url)
        err = excinfo.value
        assert err.code == 404
        assert err.response is not None
        assert err.response.code == 404
        assert err.response.body == b"Not found"
    finally:
        client.close()
        server.stop()

@pytest.mark.asyncio
async def test_close_releases_resources(tmp_path):
    """After close, the client should not be usable and the IOLoop should be closed."""
    server, port = start_test_server(DelayedHandler)
    client = httpclient.HTTPClient()
    client.close()
    # After close, attempting to fetch should raise RuntimeError due to closed IOLoop
    url = f"http://127.0.0.1:{port}/"
    with pytest.raises(RuntimeError):
        client.fetch(url)
    # Ensure the server is still running (so we didn't close it inadvertently)
    server.stop()
