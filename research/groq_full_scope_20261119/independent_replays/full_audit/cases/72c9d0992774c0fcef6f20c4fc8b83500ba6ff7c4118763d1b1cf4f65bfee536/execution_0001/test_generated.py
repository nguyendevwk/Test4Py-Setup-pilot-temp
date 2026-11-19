import pytest
import base64
from flutils.codecs.b64 import encode

def test_encode_normal_single_line():
    # A simple base64 string without whitespace
    b64_str = "SGVsbG8gV29ybGQh"  # "Hello World!"
    decoded, length = encode(b64_str)
    assert decoded == b"Hello World!"
    assert length == len(b64_str)

def test_encode_with_whitespace_and_newlines():
    # Base64 string split across lines with indentation
    b64_str = """
        SGVsbG8g
        V29ybGQh
    """
    decoded, length = encode(b64_str)
    assert decoded == b"Hello World!"
    # length should be the original string length (including whitespace)
    assert length == len(b64_str)

def test_encode_invalid_base64_raises_unicode_encode_error():
    # Invalid base64 characters should raise UnicodeEncodeError
    invalid_b64 = "!!!invalid!!!"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(invalid_b64)
    # Ensure the error message contains the cleaned string
    assert "!!!invalid!!!" in str(excinfo.value)
