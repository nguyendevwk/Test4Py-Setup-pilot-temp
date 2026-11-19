import zlib
import pytest
from tornado.util import GzipDecompressor


def test_normal_decompression(tmp_path):
    # Create a gzip-compressed byte string
    original = b"Hello, world! " * 10
    compressor = zlib.compressobj(level=9, method=zlib.DEFLATED,
                                  wbits=16 + zlib.MAX_WBITS)
    compressed = compressor.compress(original) + compressor.flush()

    # Decompress using GzipDecompressor
    decompressor = GzipDecompressor()
    chunk = decompressor.decompress(compressed)
    assert chunk == original
    assert decompressor.unconsumed_tail == b""
    assert decompressor.flush() == b""


def test_max_length_boundary(tmp_path):
    # Compress a known string
    original = b"Boundary test data" * 5
    compressor = zlib.compressobj(level=6, method=zlib.DEFLATED,
                                  wbits=16 + zlib.MAX_WBITS)
    compressed = compressor.compress(original) + compressor.flush()

    # Decompress with a small max_length to force unconsumed_tail
    decompressor = GzipDecompressor()
    first_part = decompressor.decompress(compressed, max_length=10)
    assert first_part == original[:10]
    tail = decompressor.unconsumed_tail
    assert tail != b""
    # Feed the remaining tail
    second_part = decompressor.decompress(tail)
    assert second_part == original[10:]
    assert decompressor.unconsumed_tail == b""
    assert decompressor.flush() == b""


def test_truncated_input_raises(tmp_path):
    # Create a gzip stream and truncate it
    original = b"Truncated data test"
    compressor = zlib.compressobj(level=6, method=zlib.DEFLATED,
                                  wbits=16 + zlib.MAX_WBITS)
    compressed = compressor.compress(original) + compressor.flush()
    truncated = compressed[:-5]  # remove last 5 bytes

    decompressor = GzipDecompressor()
    decompressor.decompress(truncated)
    with pytest.raises(zlib.error):
        decompressor.flush()
