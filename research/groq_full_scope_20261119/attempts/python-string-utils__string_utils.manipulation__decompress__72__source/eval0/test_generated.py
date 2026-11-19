import pytest
import base64
import zlib
from string_utils.manipulation import decompress, compress
from string_utils.errors import InvalidInputError

def test_decompress_roundtrip():
    original = "The quick brown fox jumps over the lazy dog 1234567890"
    compressed = compress(original)
    decompressed = decompress(compressed)
    assert decompressed == original
    assert isinstance(decompressed, str)

def test_decompress_empty_string():
    original = ""
    compressed = compress(original)
    decompressed = decompress(compressed)
    assert decompressed == original
    assert decompressed == ""

def test_decompress_invalid_input():
    # Create a string that is not a valid base64-encoded zlib payload
    invalid = "not-a-valid-base64-string!!"
    with pytest.raises(InvalidInputError):
        decompress(invalid)
