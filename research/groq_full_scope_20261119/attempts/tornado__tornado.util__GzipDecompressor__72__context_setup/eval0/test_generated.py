import gzip
import zlib
import pytest
from tornado.util import GzipDecompressor


def test_normal_decompression(tmp_path):
    # Create a small gzip file
    original = b"Hello, world! " * 10
    compressed_path = tmp_path / "test.gz"
    with gzip.open(compressed_path, "wb") as f:
        f.write(original)

    # Read compressed data in chunks
    decompressor = GzipDecompressor()
    decompressed = b""
    with open(compressed_path, "rb") as f:
        while True:
            chunk = f.read(15)  # arbitrary chunk size
            if not chunk:
                break
            decompressed += decompressor.decompress(chunk)
    decompressed += decompressor.flush()

    assert decompressed == original
    assert decompressor.unconsumed_tail == b""


def test_max_length_and_unconsumed_tail(tmp_path):
    # Compress data that is larger than the max_length we will use
    original = b"A" * 100
    compressed_path = tmp_path / "test2.gz"
    with gzip.open(compressed_path, "wb") as f:
        f.write(original)

    decompressor = GzipDecompressor()
    with open(compressed_path, "rb") as f:
        # Read the entire compressed file at once
        compressed = f.read()

    # Decompress with a small max_length to force unconsumed_tail
    part1 = decompressor.decompress(compressed, max_length=50)
    tail = decompressor.unconsumed_tail
    assert len(part1) > 0
    assert tail != b""

    # Feed the remaining tail back in
    part2 = decompressor.decompress(tail)
    result = part1 + part2 + decompressor.flush()

    assert result == original
    assert decompressor.unconsumed_tail == b""


def test_truncated_input_raises_error(tmp_path):
    # Create a valid gzip file
    original = b"Test data for error case."
    compressed_path = tmp_path / "test3.gz"
    with gzip.open(compressed_path, "wb") as f:
        f.write(original)

    # Read compressed data and truncate it
    with open(compressed_path, "rb") as f:
        compressed = f.read()
    truncated = compressed[:-5]  # remove last 5 bytes

    decompressor = GzipDecompressor()
    # Decompressing truncated data should raise zlib.error on flush
    decompressor.decompress(truncated)
    with pytest.raises(zlib.error):
        decompressor.flush()
