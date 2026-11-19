import pytest
from tornado.httpclient import HTTPResponse, HTTPError, httputil, HTTPRequest


def test_success_response_body_and_no_error():
    """A 200 response should expose its body and have no error."""
    body_bytes = b"hello world"
    buffer = BytesIO(body_bytes)
    req = HTTPRequest(url="http://example.com")
    resp = HTTPResponse(request=req, code=200, buffer=buffer)

    # Body is read lazily from the buffer
    assert resp.body == body_bytes
    # Subsequent accesses return the cached value
    assert resp.body is resp._body

    # No error should be set for a 2xx status
    assert resp.error is None
    # rethrow should not raise
    resp.rethrow()


def test_error_response_auto_error_and_reason():
    """A non‑2xx status should automatically create an HTTPError."""
    req = HTTPRequest(url="http://example.com")
    resp = HTTPResponse(request=req, code=404)

    # The error should be an HTTPError with the correct code and message
    assert isinstance(resp.error, HTTPError)
    assert resp.error.code == 404
    assert resp.error.message == httputil.responses.get(404, "Unknown")

    # The reason attribute should default to the standard reason phrase
    assert resp.reason == httputil.responses.get(404, "Unknown")

    # rethrow should raise the stored HTTPError
    with pytest.raises(HTTPError) as excinfo:
        resp.rethrow()
    assert excinfo.value is resp.error


def test_custom_error_overrides_auto_error():
    """Providing an explicit error should override the automatic one."""
    class DummyError(Exception):
        pass

    req = HTTPRequest(url="http://example.com")
    dummy_err = DummyError("custom")
    resp = HTTPResponse(request=req, code=500, error=dummy_err)

    # The error should be the one we passed in, not an HTTPError
    assert resp.error is dummy_err
    assert not isinstance(resp.error, HTTPError)

    # The reason should still be set from the status code
    assert resp.reason == httputil.responses.get(500, "Unknown")

    # rethrow should raise the custom error
    with pytest.raises(DummyError):
        resp.rethrow()
