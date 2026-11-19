import argparse
import http.server
import socket
import threading
import time
from http import HTTPStatus
from pathlib import Path

import pytest
import requests

from httpie.client import collect_messages
from httpie.context import Environment


def _start_http_server(handler_class, port):
    server = http.server.HTTPServer(("127.0.0.1", port), handler_class)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"hello")

    def log_message(self, format, *args):
        pass  # suppress logging


class RedirectHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", "/")
        self.end_headers()

    def log_message(self, format, *args):
        pass


@pytest.fixture
def env(tmp_path: Path):
    return Environment(config=tmp_path)


def _make_args(url, **kwargs):
    ns = argparse.Namespace(
        method="GET",
        url=url,
        headers={},
        files=None,
        data=None,
        json=False,
        form=False,
        multipart=False,
        boundary=None,
        auth=None,
        auth_plugin=None,
        auth_type=None,
        raw_auth=None,
        params={},
        timeout=None,
        verify="yes",
        cert=None,
        cert_key=None,
        cert_key_pass=None,
        proxy=[],
        max_redirects=None,
        follow=False,
        all=False,
        offline=False,
        chunked=False,
        path_as_is=False,
        compress=0,
        debug=False,
        session=None,
        session_read_only=None,
        max_headers=None,
    )
    ns.__dict__.update(kwargs)
    return ns


def test_collect_messages_yields_request_and_response(env, tmp_path):
    port = 8000
    server, thread = _start_http_server(SimpleHandler, port)
    try:
        url = f"http://127.0.0.1:{port}/"
        args = _make_args(url)
        msgs = list(collect_messages(env, args))
        assert len(msgs) == 2
        request, response = msgs
        assert isinstance(request, requests.PreparedRequest)
        assert request.method == "GET"
        assert request.url == url
        assert isinstance(response, requests.Response)
        assert response.status_code == 200
        assert response.text == "hello"
    finally:
        server.shutdown()
        thread.join()


def test_path_as_is_preserves_original_path(env, tmp_path):
    port = 8001
    server, thread = _start_http_server(SimpleHandler, port)
    try:
        original_url = f"http://127.0.0.1:{port}/../"
        args = _make_args(original_url, path_as_is=True)
        msgs = list(collect_messages(env, args))
        request, response = msgs
        assert request.url == original_url
        assert response.status_code == 200
    finally:
        server.shutdown()
        thread.join()


def test_max_redirects_raises_too_many_redirects(env, tmp_path):
    port = 8002
    server, thread = _start_http_server(RedirectHandler, port)
    try:
        url = f"http://127.0.0.1:{port}/"
        args = _make_args(url, follow=True, max_redirects=1)
        with pytest.raises(requests.TooManyRedirects):
            list(collect_messages(env, args))
    finally:
        server.shutdown()
        thread.join()
