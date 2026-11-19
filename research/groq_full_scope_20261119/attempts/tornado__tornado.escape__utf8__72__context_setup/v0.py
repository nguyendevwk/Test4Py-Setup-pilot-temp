import pytest
from tornado.escape import utf8, _UTF8_TYPES
from typing import Union

def test_utf8_returns_bytes_when_input_is_bytes_or_none() -> None:
    # Bytes input should be returned unchanged
    data_bytes: bytes = b"hello"
    assert utf8(data_bytes) is data_bytes
    # None input should be returned unchanged
    assert utf8(None) is None

def test_utf8_encodes_unicode_string_to_utf8_bytes() -> None:
    # Unicode string should be encoded to UTF-8 bytes
    text: str = "café"
    encoded: bytes = utf8(text)
    assert isinstance(encoded, bytes)
    assert encoded == text.encode("utf-8")
    # Ensure that the returned bytes are not the same object as the original string
    assert encoded != text

def test_utf8_raises_type_error_for_invalid_input() -> None:
    # Passing an integer should raise a TypeError
    with pytest.raises(TypeError) as excinfo:
        utf8(42)  # type: ignore[arg-type]
    assert "Expected bytes, unicode, or None" in str(excinfo.value)
    # Passing a list should also raise a TypeError
    with pytest.raises(TypeError):
        utf8([1, 2, 3])  # type: ignore[arg-type]
