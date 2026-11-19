import base64
import pytest
from flutils.codecs.b64 import encode

def test_encode_normal():
    # A simple base64 string without whitespace
    original = b"hello world"
    b64_str = base64.b64encode(original).decode()
    decoded, length = encode(b64_str)
    assert decoded == original
    assert length == len(b64_str)

def test_encode_with_whitespace_and_newlines():
    # Base64 string split across lines with indentation
    original = b"foo bar baz"
    b64_str = base64.b64encode(original).decode()
    # Insert newlines and spaces
    formatted = f"  {b64_str[:4]}\n{b64_str[4:8]}\n   {b64_str[8:]}"
    decoded, length = encode(formatted)
    assert decoded == original
    assert length == len(formatted)

def test_encode_invalid_base64_raises():
    # String containing invalid base64 characters
    invalid = "!!!invalid!!!"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(invalid)
    assert "not a proper bas64 character string" in str(excinfo.value)
