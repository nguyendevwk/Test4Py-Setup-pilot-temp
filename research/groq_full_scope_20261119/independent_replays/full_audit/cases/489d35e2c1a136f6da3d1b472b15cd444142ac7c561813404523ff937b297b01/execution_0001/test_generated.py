import pytest
import base64
from flutils.codecs.b64 import encode

def test_encode_normal():
    # A simple base64 string without whitespace
    original = b"Hello, World!"
    b64_str = base64.b64encode(original).decode()
    decoded, length = encode(b64_str)
    assert decoded == original
    assert length == len(b64_str)

def test_encode_with_whitespace_and_newlines():
    # Base64 string split across lines with indentation
    original = b"Python is fun!"
    b64_bytes = base64.b64encode(original)
    # Insert newlines and spaces
    b64_str = (
        "   " + b64_bytes[:5].decode() + "\n"
        "  " + b64_bytes[5:10].decode() + "\n"
        "   " + b64_bytes[10:].decode() + "   "
    )
    decoded, length = encode(b64_str)
    assert decoded == original
    assert length == len(b64_str)

def test_encode_invalid_base64_raises_unicodeencodeerror():
    # Invalid base64 string (contains non-base64 character)
    bad_str = "!!!invalid!!!"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(bad_str)
    # Ensure the exception message references the problematic string
    assert "not a proper bas64 character string" in str(excinfo.value)
    assert bad_str in str(excinfo.value)
