import pytest
from tornado.httpclient import HTTPError
from tornado.httpclient import main as httpclient_main
from tornado.httpclient import HTTPClient
from tornado.options import options


class DummyResponse:
    def __init__(self, headers, body):
        self.headers = headers
        self.body = body


class DummyClient:
    def __init__(self, responses):
        self._responses = responses
        self._calls = []

    def fetch(self, url, **kwargs):
        self._calls.append((url, kwargs))
        resp = self._responses.pop(0)
        if isinstance(resp, Exception):
            raise resp
        return resp

    def close(self):
        pass


def test_main_prints_headers_and_body(monkeypatch, capsys):
    # Arrange
    dummy_resp = DummyResponse(headers="X-Test: 123", body=b"Hello")
    dummy_client = DummyClient([dummy_resp])

    monkeypatch.setattr(httpclient_main, "HTTPClient", lambda: dummy_client)
    monkeypatch.setattr(httpclient_main, "parse_command_line", lambda: ["http://example.com"])
    options.print_headers = True
    options.print_body = True

    # Act
    httpclient_main.main()

    # Assert
    out, err = capsys.readouterr()
    assert "X-Test: 123" in out
    assert "Hello" in out
    assert dummy_client._calls == [("http://example.com", {
        'follow_redirects': options.follow_redirects,
        'validate_cert': options.validate_cert,
        'proxy_host': options.proxy_host,
        'proxy_port': options.proxy_port,
    })]


def test_main_handles_http_error_with_response(monkeypatch, capsys):
    # Arrange
    dummy_resp = DummyResponse(headers="X-Error: 404", body=b"Not Found")
    http_error = HTTPError(404, response=dummy_resp)
    dummy_client = DummyClient([http_error])

    monkeypatch.setattr(httpclient_main, "HTTPClient", lambda: dummy_client)
    monkeypatch.setattr(httpclient_main, "parse_command_line", lambda: ["http://example.com"])
    options.print_headers = True
    options.print_body = True

    # Act
    httpclient_main.main()

    # Assert
    out, err = capsys.readouterr()
    assert "X-Error: 404" in out
    assert "Not Found" in out
    assert dummy_client._calls == [("http://example.com", {
        'follow_redirects': options.follow_redirects,
        'validate_cert': options.validate_cert,
        'proxy_host': options.proxy_host,
        'proxy_port': options.proxy_port,
    })]


def test_main_raises_http_error_without_response(monkeypatch):
    # Arrange
    http_error = HTTPError(500, response=None)
    dummy_client = DummyClient([http_error])

    monkeypatch.setattr(httpclient_main, "HTTPClient", lambda: dummy_client)
    monkeypatch.setattr(httpclient_main, "parse_command_line", lambda: ["http://example.com"])
    options.print_headers = False
    options.print_body = False

    # Act & Assert
    with pytest.raises(HTTPError) as excinfo:
        httpclient_main.main()
    assert excinfo.value is http_error
    assert dummy_client._calls == [("http://example.com", {
        'follow_redirects': options.follow_redirects,
        'validate_cert': options.validate_cert,
        'proxy_host': options.proxy_host,
        'proxy_port': options.proxy_port,
    })]
