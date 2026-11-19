import pytest
from string_utils.manipulation import decompress, __StringCompressor
from string_utils.errors import InvalidInputError

def test_decompress_normal():
    original = "The quick brown fox jumps over the lazy dog 1234567890"
    compressed = __StringCompressor.compress(original, encoding="utf-8", compression_level=6)
    result = decompress(compressed, encoding="utf-8")
    assert result == original
    assert isinstance(result, str)

def test_decompress_empty_input_raises_value_error():
    with pytest.raises(ValueError) as excinfo:
        decompress("", encoding="utf-8")
    assert "Input string cannot be empty" in str(excinfo.value)

def test_decompress_invalid_encoding_raises_value_error():
    compressed = __StringCompressor.compress("test", encoding="utf-8")
    with pytest.raises(ValueError) as excinfo:
        decompress(compressed, encoding=123)  # non-string encoding
    assert "Invalid encoding" in str(excinfo.value)
