import pytest
from string_utils.manipulation import decompress
from string_utils.errors import InvalidInputError

def test_decompress_normal():
    # Compress a known string using the public API and then decompress it
    original = "The quick brown fox jumps over the lazy dog 1234567890"
    # Use the internal compressor directly to get a compressed string
    from string_utils.manipulation import __StringCompressor
    compressed = __StringCompressor.compress(original, encoding="utf-8", compression_level=6)
    # Decompress using the public function
    result = decompress(compressed, encoding="utf-8")
    assert result == original
    assert isinstance(result, str)

def test_decompress_empty_input_raises_value_error():
    # An empty string should raise a ValueError according to the implementation
    with pytest.raises(ValueError) as excinfo:
        decompress("", encoding="utf-8")
    assert "Input string cannot be empty" in str(excinfo.value)

def test_decompress_invalid_encoding_raises_value_error():
    # Passing a non-string encoding should raise a ValueError
    from string_utils.manipulation import __StringCompressor
    original = "sample text"
    compressed = __StringCompressor.compress(original, encoding="utf-8")
    with pytest.raises(ValueError) as excinfo:
        decompress(compressed, encoding=123)  # invalid encoding type
    assert "Invalid encoding" in str(excinfo.value)
