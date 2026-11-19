import pytest
from string_utils.manipulation import compress, decompress
from string_utils.errors import InvalidInputError

def test_compress_and_decompress_roundtrip():
    original = " ".join([f"word n{i}" for i in range(20)])
    compressed = compress(original, compression_level=9)
    # compressed should be shorter than original
    assert len(compressed) < len(original)
    # decompress should recover the original
    recovered = decompress(compressed)
    assert recovered == original

def test_compress_empty_string_raises():
    with pytest.raises(ValueError):
        compress("")

def test_compress_invalid_compression_level_raises():
    with pytest.raises(ValueError):
        compress("some text", compression_level=10)
    with pytest.raises(ValueError):
        compress("some text", compression_level=-1)
