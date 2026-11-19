import pytest
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
    with pytest.raises(InvalidInputError):
        decompress(None)
