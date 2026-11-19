import pytest
from string_utils.manipulation import compress, decompress
from string_utils.errors import InvalidInputError

def test_compress_and_decompress_roundtrip():
    original = " ".join([f"word n{i}" for i in range(20)])
    compressed = compress(original)
    assert isinstance(compressed, str)
    assert compressed != original  # should be shorter or different
    recovered = decompress(compressed)
    assert recovered == original

def test_compress_empty_string_raises_value_error():
    with pytest.raises(ValueError):
        compress("")

def test_compress_level_zero_no_compression():
    original = "abcabcabcabcabcabcabcabcabcabc"
    compressed = compress(original, compression_level=0)
    # With level 0, zlib does not compress, so the output should be longer than input
    assert len(compressed) > len(original)
    recovered = decompress(compressed)
    assert recovered == original
