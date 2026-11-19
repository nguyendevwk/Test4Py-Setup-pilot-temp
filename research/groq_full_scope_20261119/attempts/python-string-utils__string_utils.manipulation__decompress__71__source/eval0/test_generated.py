import pytest
import base64
import zlib
from string_utils.manipulation import decompress, compress
from string_utils.errors import InvalidInputError

def test_decompress_roundtrip(tmp_path):
    """Normal case: compress then decompress returns original string."""
    original = "The quick brown fox jumps over the lazy dog 1234567890"
    compressed = compress(original)
    # Ensure compressed is a string and not equal to original
    assert isinstance(compressed, str)
    assert compressed != original
    # Decompress and compare
    decompressed = decompress(compressed)
    assert decompressed == original

def test_decompress_empty_string(tmp_path):
    """Boundary case: empty string should round‑trip correctly."""
    original = ""
    compressed = compress(original)
    assert isinstance(compressed, str)
    assert compressed != original
    decompressed = decompress(compressed)
    assert decompressed == original

def test_decompress_invalid_input():
    """Error case: passing a non‑compressed string should raise InvalidInputError."""
    # Create a string that is not a valid base64 zlib payload
    invalid = "not-a-valid-compressed-string"
    with pytest.raises(InvalidInputError):
        decompress(invalid)
