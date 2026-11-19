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
    with open(compressed_path, "rb") as f:
        chunk = f.read(32)
        while chunk:
            decompressed = decompressor.decompress(chunk)
            assert decompressed == original[: len(decompressed)]
            original = original[len(decompressed) :]
            chunk = f.read(32)

    # Flush remaining data
    remaining = decompressor.flush()
    assert remaining == original
    assert decompressor.unconsumed_tail == b""


def test_max_length_boundary(tmp_path):
    # Compress data larger than a single chunk
    original = b"Boundary test data " * 20
    compressed_path = tmp_path / "boundary.gz"
    with gzip.open(compressed_path, "wb") as f:
        f.write(original)

    decompressor = GzipDecompressor()
    with open(compressed_path, "rb") as f:
        # Read a chunk that will be partially consumed
        chunk = f.read(50)
        # Decompress with a small max_length to force unconsumed_tail
        part = decompressor.decompress(chunk, max_length=10)
        assert len(part) <= 10
        # The remaining data should be in unconsumed_tail
        tail = decompressor.unconsumed_tail
        assert tail != b""
        # Pass the tail back to decompress
        part2 = decompressor.decompress(tail)
        # Combine parts and compare to original
        assert part + part2 == original[: len(part) + len(part2)]

    # Flush to get any remaining data
    remaining = decompressor.flush()
    assert remaining == original[len(part) + len(part2) :]


def test_truncated_input_error():
    # Create a valid gzip stream
    original = b"Error test data " * 5
    compressed = gzip.compress(original)

    # Truncate the compressed data to simulate corruption
    truncated = compressed[:-10]

    decompressor = GzipDecompressor()
    # Decompressing truncated data should raise zlib.error on flush
    decompressor.decompress(truncated)
    with pytest.raises(zlib.error):
        decompressor.flush()
