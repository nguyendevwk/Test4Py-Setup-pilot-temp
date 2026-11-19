import io
import os
import sys
import pytest
from httpie.output.writer import write_stream_with_colors_win
from httpie.output.streams import BaseStream

class DummyStream(BaseStream):
    """A minimal BaseStream that yields predefined byte chunks."""
    def __init__(self, chunks):
        self._chunks = chunks
        self._iter = iter(chunks)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)

def test_write_stream_with_colors_win_writes_color_and_non_color_chunks(tmp_path):
    # Prepare chunks: one with ANSI escape, one plain
    color_chunk = b'\x1b[31mRed text\x1b[0m'
    plain_chunk = b'Plain text'
    stream = DummyStream([color_chunk, plain_chunk])

    # Create a text file with a BytesIO buffer
    file_path = tmp_path / "output.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        # Write the stream to the file
        write_stream_with_colors_win(stream, f, flush=False)

    # Read back the file content
    with open(file_path, "rb") as f:
        content = f.read()

    # The color chunk should be decoded to text and written as UTF-8 bytes
    expected_text = color_chunk.decode("utf-8")
    # The plain chunk should be written directly to the buffer
    expected_bytes = plain_chunk
    assert content == expected_text.encode("utf-8") + expected_bytes

def test_write_stream_with_colors_win_flush_behavior(tmp_path):
    # Two chunks, both non-color
    chunk1 = b'First'
    chunk2 = b'Second'
    stream = DummyStream([chunk1, chunk2])

    file_path = tmp_path / "flush.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        # Flush after each chunk
        write_stream_with_colors_win(stream, f, flush=True)

    # After writing, the file should contain both chunks concatenated
    with open(file_path, "rb") as f:
        content = f.read()
    assert content == chunk1 + chunk2

def test_write_stream_with_colors_win_handles_empty_stream(tmp_path):
    # Empty stream should produce no output
    stream = DummyStream([])

    file_path = tmp_path / "empty.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        write_stream_with_colors_win(stream, f, flush=False)

    # File should be empty
    assert file_path.read_bytes() == b''
