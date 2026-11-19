import pytest
import base64
from flutils.codecs.b64 import encode


def test_encode_normal():
    """Test that a simple base64 string is decoded correctly."""
    # "Hello, world!" encoded in base64
    b64_str = "SGVsbG8sIHdvcmxkIQ=="
    decoded, length = encode(b64_str)
    assert decoded == b"Hello, world!"
    assert length == len(b64_str)


def test_encode_boundary_empty():
    """Test that an empty string returns an empty bytes object."""
    decoded, length = encode("")
    assert decoded == b""
    assert length == 0


def test_encode_error_invalid_char():
    """Test that an invalid base64 string raises UnicodeEncodeError."""
    invalid_b64 = "!!!invalid!!!"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(invalid_b64)
    # The exception message should mention the problematic string
    assert "is not a proper bas64 character string" in str(excinfo.value)
    # The original input should be present in the exception
    assert invalid_b64 in str(excinfo.value)
