import pytest
import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.gen
import asyncio

# Helper to run a simple Tornado server in a background thread
@pytest.fixture
def http_server(tmp_path):
    class TestHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("Hello, world!")

    class RedirectHandler(tornado.web.RequestHandler):
        def get(self):
            self.redirect("/hello")

    app = tornado.web.Application(
        [
            (r"/hello", TestHandler),
            (r"/redirect", RedirectHandler),
        ]
    )
    server = app.listen(0)  # bind to an arbitrary free port
    port = server.get_socket().getsockname()[1]
    loop = tornado.ioloop.IOLoop.current()
    # Run the IOLoop in a separate thread
    thread = tornado.ioloop.IOLoop.current().start()
    yield f"http://localhost:{port}"
    server.stop()
    loop.stop()


def test_fetch_success(http_server):
    client = tornado.httpclient.HTTPClient()
    try:
        response = client.fetch(http_server + "/hello")
        assert response.code == 200
        assert response.body == b"Hello, world!"
    finally:
        client.close()


def test_fetch_not_found(http_server):
    client = tornado.httpclient.HTTPClient()
    try:
        with pytest.raises(tornado.httpclient.HTTPError) as excinfo:
            client.fetch(http_server + "/nonexistent")
        err = excinfo.value
        assert err.code == 404
        assert err.response is not None
        assert err.response.code == 404
    finally:
        client.close()


def test_redirect_handling(http_server):
    client = tornado.httpclient.HTTPClient()
    try:
        # By default follow_redirects=True, so we get the final 200
        response = client.fetch(http_server + "/redirect")
        assert response.code == 200
        assert response.body == b"Hello, world!"

        # Disable redirects; should raise HTTPError with 302 response
        with pytest.raises(tornado.httpclient.HTTPError) as excinfo:
            client.fetch(
                http_server + "/redirect",
                follow_redirects=False,
            )
        err = excinfo.value
        assert err.code == 302
        assert err.response is not None
        assert err.response.code == 302
        assert err.response.headers.get("Location") == "/hello"
    finally:
        client.close()
