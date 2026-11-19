import gzip
import zlib
import pytest
from tornado.util import GzipDecompressor


def test_decompress_full_stream(tmp_path):
    """Decompress a complete gzip stream and verify the output."""
    original = b"Hello, world! " * 1000
    compressed = gzip.compress(original)

    decompressor = GzipDecompressor()
    # Decompress in a single call
    result = decompressor.decompress(compressed)
    # Flush to get any remaining data
    result += decompressor.flush()

    assert result == original
    assert decompressor.unconsumed_tail == b""


def test_decompress_with_max_length(tmp_path):
    """Decompress with a max_length that forces unconsumed_tail to be non‑empty."""
    original = b"abc" * 500
    compressed = gzip.compress(original)

    decompressor = GzipDecompressor()
    # Decompress only a small chunk
    part1 = decompressor.decompress(compressed[:10], max_length=5)
    part2 = decompressor.decompress(decompressor.unconsumed_tail, max_length=5)
    # Continue until all data is processed
    remaining = decompressor.decompress(compressed[10:], max_length=0)
    remaining += decompressor.flush()

    assert part1 + part2 + remaining == original
    assert decompressor.unconsumed_tail == b""


def test_decompress_truncated_input_raises():
    """Decompressing a truncated gzip stream should raise an error on flush."""
    original = b"data that will be truncated"
    compressed = gzip.compress(original)

    # Truncate the compressed data to simulate corruption
    truncated = compressed[:-10]

    decompressor = GzipDecompressor()
    decompressor.decompress(truncated)
    with pytest.raises(zlib.error):
        decompressor.flush()
