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

def test_compress_empty_string_raises():
    with pytest.raises(ValueError):
        compress("")

def test_compress_level_zero_no_compression():
    original = "aaaaabbbbbcccccdddddeeeee"
    compressed_level_9 = compress(original, compression_level=9)
    compressed_level_0 = compress(original, compression_level=0)
    # Level 0 should produce a string that is not shorter than level 9
    assert len(compressed_level_0) >= len(compressed_level_9)
    # Decompress both to verify they recover the same original
    assert decompress(compressed_level_9) == original
    assert decompress(compressed_level_0) == original
