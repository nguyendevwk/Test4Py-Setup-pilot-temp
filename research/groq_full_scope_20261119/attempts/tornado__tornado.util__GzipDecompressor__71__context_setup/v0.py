import zlib
import pytest
from tornado.util import GzipDecompressor


def test_decompress_full_stream(tmp_path):
    # Create a gzip-compressed byte string
    original = b"Hello, world! " * 10
    compressed = zlib.compress(original, level=9, wbits=16 + zlib.MAX_WBITS)

    # Decompress using GzipDecompressor
    decompressor = GzipDecompressor()
    chunk = decompressor.decompress(compressed)
    # All data should be returned in one call
    assert chunk == original
    # No unconsumed tail
    assert decompressor.unconsumed_tail == b""
    # Flush should return empty bytes
    assert decompressor.flush() == b""


def test_decompress_with_max_length(tmp_path):
    # Create a gzip-compressed byte string
    original = b"Boundary test data " * 5
    compressed = zlib.compress(original, level=6, wbits=16 + zlib.MAX_WBITS)

    # Decompress with a small max_length to force unconsumed_tail
    decompressor = GzipDecompressor()
    first_part = decompressor.decompress(compressed, max_length=10)
    # First part should be at most 10 bytes
    assert len(first_part) <= 10
    # There should be remaining data
    assert decompressor.unconsumed_tail != b""
    # Decompress the remaining tail
    second_part = decompressor.decompress(decompressor.unconsumed_tail)
    # Combined result should match original
    assert first_part + second_part == original
    # Flush should be empty
    assert decompressor.flush() == b""


def test_decompress_truncated_stream(tmp_path):
    # Create a gzip-compressed byte string and truncate it
    original = b"Truncated data test " * 3
    compressed = zlib.compress(original, level=5, wbits=16 + zlib.MAX_WBITS)
    truncated = compressed[:-5]  # remove last 5 bytes

    decompressor = GzipDecompressor()
    # Decompress the truncated data; it may return some bytes
    partial = decompressor.decompress(truncated)
    # The partial result should be a prefix of the original
    assert partial == original[: len(partial)]
    # Flush should raise an error due to incomplete gzip stream
    with pytest.raises(zlib.error):
        decompressor.flush()
