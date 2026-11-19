import argparse
import gzip
import json
import os
import tempfile
from pathlib import Path

import pytest
import requests

from httpie.client import collect_messages
from httpie.context import Environment
from httpie.models import RequestsMessage


@pytest.fixture
def env(tmp_path):
    """Create a minimal Environment for testing."""
    env = Environment()
    env.config.directory = tmp_path
    return env


def make_args(url="http://example.com", method="GET", headers=None, **kwargs):
    """Helper to build argparse.Namespace for collect_messages."""
    ns = argparse.Namespace(
        url=url,
        method=method,
        headers=headers or {},
        session=None,
        session_read_only=None,
        auth_plugin=None,
        debug=False,
        path_as_is=False,
        compress=0,
        offline=False,
        follow=False,
        all=False,
        max_redirects=None,
        max_headers=200,
        ssl_version=None,
        ciphers=None,
        verify=True,
        **kwargs,
    )
    return ns


def test_collect_messages_basic(env):
    """Collect a simple GET request and verify request properties."""
    args = make_args(url="http://example.com/api", method="GET")
    messages = list(collect_messages(env, args, request_body_read_callback=None))
    # Should yield only the prepared request (offline default False but no send)
    assert len(messages) == 1
    req = messages[0]
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == "GET"
    assert req.url == "http://example.com/api"
    # Default headers include User-Agent from httpie
    assert "User-Agent" in req.headers
    assert req.body is None


def test_collect_messages_offline(env):
    """When offline, only the request is yielded and no response is sent."""
    args = make_args(url="http://example.com/api", method="GET", offline=True)
    messages = list(collect_messages(env, args, request_body_read_callback=None))
    assert len(messages) == 1
    req = messages[0]
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == "GET"
    assert req.url == "http://example.com/api"
    # No response should be present
    assert all(isinstance(m, requests.PreparedRequest) for m in messages)


def test_collect_messages_compress_body(env):
    """When compress is enabled, the request body is gzip-compressed."""
    body = b"Hello, world!"
    args = make_args(url="http://example.com/api", method="POST", compress=1)

    def body_callback(b):
        # Simulate reading body from stdin
        return body

    # Prepare arguments to include data
    args.data = body
    args.headers = {"Content-Type": "text/plain"}

    messages = list(collect_messages(env, args, request_body_read_callback=body_callback))
    assert len(messages) == 1
    req = messages[0]
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == "POST"
    assert req.url == "http://example.com/api"
    # Body should be gzip compressed
    decompressed = gzip.decompress(req.body)
    assert decompressed == body
    # Content-Encoding header should be set
    assert req.headers.get("Content-Encoding") == "gzip"
