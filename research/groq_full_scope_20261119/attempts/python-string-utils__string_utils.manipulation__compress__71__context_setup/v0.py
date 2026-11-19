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

def test_compression_level_bounds():
    text = "repeat " * 10
    # level 0: no compression
    no_compress = compress(text, compression_level=0)
    # level 9: best compression
    best_compress = compress(text, compression_level=9)
    assert isinstance(no_compress, str) and isinstance(best_compress, str)
    assert len(best_compress) <= len(no_compress)
    assert decompress(no_compress) == text
    assert decompress(best_compress) == text

def test_invalid_inputs_raise_errors():
    with pytest.raises(ValueError, match="Input string cannot be empty"):
        compress("")
    with pytest.raises(ValueError, match="Invalid compression_level"):
        compress("sample", compression_level=10)
    with pytest.raises(ValueError, match="Invalid compression_level"):
        compress("sample", compression_level=-1)
    with pytest.raises(ValueError, match="Invalid encoding"):
        compress("sample", encoding=123)  # non-string encoding
    with pytest.raises(InvalidInputError):
        compress(123)  # non-string input
