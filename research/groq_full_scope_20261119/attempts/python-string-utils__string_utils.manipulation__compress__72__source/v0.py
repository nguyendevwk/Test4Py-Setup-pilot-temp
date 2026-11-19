import pytest
from string_utils.manipulation import compress, decompress, InvalidInputError

def test_compress_and_decompress_roundtrip():
    original = "word n0 " * 20  # 20 repetitions, 169 chars
    compressed = compress(original)
    # compressed should be shorter than original
    assert len(compressed) < len(original)
    # decompress should recover the original string
    recovered = decompress(compressed)
    assert recovered == original

def test_compress_empty_string_raises():
    with pytest.raises(ValueError):
        compress("")  # empty input should raise ValueError

def test_compress_invalid_compression_level_raises():
    # compression_level must be between 0 and 9 inclusive
    with pytest.raises(InvalidInputError):
        compress("some text", compression_level=10)
    with pytest.raises(InvalidInputError):
        compress("some text", compression_level=-1)
