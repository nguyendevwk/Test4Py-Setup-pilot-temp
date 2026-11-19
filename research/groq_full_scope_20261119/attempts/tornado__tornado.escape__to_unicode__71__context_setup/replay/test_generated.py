import pytest
from tornado.escape import to_unicode

def test_to_unicode_with_str_and_none():
    # Passing a unicode string should return the same object
    s = "hello world"
    assert to_unicode(s) is s
    # Passing None should return None unchanged
    assert to_unicode(None) is None

def test_to_unicode_with_bytes_and_decoding():
    # Bytes that are valid UTF‑8 should be decoded correctly
    b = b"hello \xe4\xbd\xa0\xe5\xa5\xbd"  # "hello 你好"
    decoded = to_unicode(b)
    assert isinstance(decoded, str)
    assert decoded == "hello 你好"

def test_to_unicode_invalid_input_and_decoding_error():
    # Non‑bytes, non‑str, non‑None should raise TypeError
    with pytest.raises(TypeError):
        to_unicode(123)
    # Bytes that are not valid UTF‑8 should raise UnicodeDecodeError
    with pytest.raises(UnicodeDecodeError):
        to_unicode(b"\xff\xfe\xfa")
