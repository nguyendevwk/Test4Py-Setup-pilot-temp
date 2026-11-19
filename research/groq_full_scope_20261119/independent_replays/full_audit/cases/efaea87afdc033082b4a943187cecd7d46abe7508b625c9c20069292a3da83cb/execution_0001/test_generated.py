import pytest
import base64
from flutils.codecs.b64 import encode

def test_encode_normal():
    # Base64 of "Hello, World!" is "SGVsbG8sIFdvcmxkIQ=="
    b64_text = "SGVsbG8sIFdvcmxkIQ=="
    decoded, length = encode(b64_text)
    assert decoded == b"Hello, World!"
    assert length == len(b64_text)

def test_encode_with_whitespace_and_newlines():
    # The function should strip whitespace and newlines
    b64_text = """
        SGVsbG8s
        IFdvcmxkIQ==
    """
    decoded, length = encode(b64_text)
    assert decoded == b"Hello, World!"
    # Length should be the original string length, including whitespace
    assert length == len(b64_text)

def test_encode_invalid_base64_raises_unicode_encode_error():
    # Provide an invalid base64 string
    invalid_b64 = "!!!invalid!!!"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(invalid_b64)
    # The exception message should mention the problematic string
    assert "not a proper bas64 character string" in str(excinfo.value)
    # The original input should be present in the exception
    assert "!!!invalid!!!" in str(excinfo.value)
