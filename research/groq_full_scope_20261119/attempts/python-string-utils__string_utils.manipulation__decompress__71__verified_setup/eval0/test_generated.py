import pytest
from string_utils.manipulation import decompress, compress
from string_utils.errors import InvalidInputError


def test_decompress_roundtrip():
    """Decompress should return the original string after a compress round‑trip."""
    original = "The quick brown fox jumps over the lazy dog 1234567890"
    compressed = compress(original)
    decompressed = decompress(compressed)
    assert decompressed == original
    assert isinstance(decompressed, str)


def test_decompress_empty_string():
    """Decompressing an empty string should yield an empty string."""
    compressed = compress("")
    decompressed = decompress(compressed)
    assert decompressed == ""
    assert decompressed == ""


def test_decompress_invalid_input():
    """Decompress should raise InvalidInputError for malformed input."""
    malformed = "not-a-valid-base64-string!!"
    with pytest.raises(InvalidInputError):
        decompress(malformed)
