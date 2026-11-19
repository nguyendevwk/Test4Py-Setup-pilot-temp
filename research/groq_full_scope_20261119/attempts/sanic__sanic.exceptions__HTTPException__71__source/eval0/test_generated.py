import pytest
from sanic.exceptions import HTTPException


def test_http_exception_basic():
    """Verify that HTTPException accepts various message types and stores them."""
    # message as string
    exc_str = HTTPException("error occurred")
    assert exc_str.message == "error occurred"
    assert exc_str.quiet is None
    assert exc_str.context is None
    assert exc_str.extra is None
    assert exc_str.headers is None

    # message as bytes
    exc_bytes = HTTPException(b"binary error")
    assert exc_bytes.message == b"binary error"

    # message as None
    exc_none = HTTPException()
    assert exc_none.message is None


def test_http_exception_headers_context_extra(tmp_path):
    """Verify that headers, context, and extra are stored correctly."""
    # Create a temporary file to use as a PathLike object in context
    temp_file = tmp_path / "dummy.txt"
    temp_file.write_text("content")

    headers = {"Content-Type": "application/json", "X-Custom": "value"}
    context = {"path": "/test", "file": temp_file}
    extra = {"code": 123}

    exc = HTTPException(
        "test",
        quiet=True,
        context=context,
        extra=extra,
        headers=headers,
    )

    assert exc.message == "test"
    assert exc.quiet is True
    assert exc.context == context
    assert exc.extra == extra
    assert exc.headers == headers
    # Ensure the PathLike object is preserved
    assert isinstance(exc.context["file"], type(temp_file))
    assert exc.context["file"].read_text() == "content"


def test_http_exception_invalid_headers():
    """Passing a non-dict to headers should raise a TypeError."""
    with pytest.raises(TypeError):
        HTTPException("error", headers="not a dict")
