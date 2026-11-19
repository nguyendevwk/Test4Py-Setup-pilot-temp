import zlib
import pytest
from tornado.util import GzipDecompressor


def test_normal_decompression(tmp_path):
    # Create a gzip-compressed byte string
    original = b"Hello, world! " * 10
    compressed = zlib.compress(original, level=9, wbits=16 + zlib.MAX_WBITS)

    # Decompress using GzipDecompressor
    dec = GzipDecompressor()
    chunk = dec.decompress(compressed)
    assert chunk == original
    assert dec.unconsumed_tail == b""
    # After all data is processed, flush should return empty
    assert dec.flush() == b""


def test_max_length_boundary(tmp_path):
    # Compress a known payload
    original = b"Boundary test data " * 5
    compressed = zlib.compress(original, level=6, wbits=16 + zlib.MAX_WBITS)

    # Decompress with a small max_length to force unconsumed_tail
    dec = GzipDecompressor()
    first_chunk = dec.decompress(compressed, max_length=10)
    # The first 10 bytes of the decompressed data should be returned
    assert first_chunk == original[:10]
    # The rest should be in unconsumed_tail
    assert dec.unconsumed_tail == original[10:]

    # Feed the remaining tail back
    second_chunk = dec.decompress(dec.unconsumed_tail)
    assert second_chunk == original[10:]
    assert dec.unconsumed_tail == b""
    assert dec.flush() == b""


def test_truncated_input_raises(tmp_path):
    # Create a valid gzip stream and then truncate it
    original = b"Truncated data test " * 3
    compressed = zlib.compress(original, level=5, wbits=16 + zlib.MAX_WBITS)
    truncated = compressed[:-5]  # remove last 5 bytes

    dec = GzipDecompressor()
    # Decompress the truncated data; it should not raise yet
    dec.decompress(truncated)
    # Flush should raise an error due to incomplete gzip stream
    with pytest.raises(zlib.error):
        dec.flush()
