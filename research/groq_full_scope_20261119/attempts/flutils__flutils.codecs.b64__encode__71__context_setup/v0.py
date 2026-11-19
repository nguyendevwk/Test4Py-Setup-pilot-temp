import base64
import pytest
from flutils.codecs.b64 import encode

def test_encode_normal():
    # A simple base64 string that decodes to b'hello world'
    b64_text = "aGVsbG8gd29ybGQ="
    decoded, length = encode(b64_text)
    assert decoded == b"hello world"
    assert length == len(b64_text)

def test_encode_with_whitespace_and_newlines():
    # Base64 string split across lines with indentation
    b64_text = """
        aGVsbG8gd29ybGQ=
    """
    decoded, length = encode(b64_text)
    assert decoded == b"hello world"
    # The length should be the length of the original string including whitespace
    assert length == len(b64_text)

def test_encode_invalid_base64_raises_unicode_encode_error():
    # Invalid base64 string (contains non-base64 character '!')
    invalid_b64 = "aGVsbG8gd29ybGQ=!"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(invalid_b64)
    # The exception message should mention the problematic string
    assert "is not a proper bas64 character string" in str(excinfo.value)
    # The original text should be present in the exception context
    assert "aGVsbG8gd29ybGQ=!" in str(excinfo.value)
