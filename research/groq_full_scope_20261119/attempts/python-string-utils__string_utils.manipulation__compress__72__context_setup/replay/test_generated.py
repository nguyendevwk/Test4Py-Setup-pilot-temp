import pytest
from string_utils.manipulation import compress, decompress
from string_utils.errors import InvalidInputError


def test_compress_and_decompress_roundtrip():
    original = "The quick brown fox jumps over the lazy dog. " * 5
    compressed = compress(original, compression_level=6)
    assert isinstance(compressed, str)
    assert compressed != original  # compression should change the string
    decompressed = decompress(compressed)
    assert decompressed == original


def test_compress_with_boundary_levels():
    text = "repeat" * 10
    # level 0: no compression
    no_compress = compress(text, compression_level=0)
    # level 9: best compression
    best_compress = compress(text, compression_level=9)
    assert isinstance(no_compress, str)
    assert isinstance(best_compress, str)
    # best compression should be shorter or equal to level 0
    assert len(best_compress) <= len(no_compress)
    # roundtrip must preserve original
    assert decompress(best_compress) == text
    assert decompress(no_compress) == text


def test_compress_errors_on_invalid_input_and_level():
    with pytest.raises(ValueError, match="Input string cannot be empty"):
        compress("", compression_level=5)
    with pytest.raises(ValueError, match="Invalid compression_level"):
        compress("data", compression_level=10)
    with pytest.raises(ValueError, match="Invalid compression_level"):
        compress("data", compression_level=-1)
    with pytest.raises(InvalidInputError):
        compress(123, compression_level=5)  # non-string input
