import io
import os
import sys
import tempfile
import pytest

from httpie.output.writer import write_stream_with_colors_win
from httpie.output.streams import BaseStream


class DummyStream(BaseStream):
    """A minimal BaseStream that yields predefined byte chunks."""
    def __init__(self, chunks):
        self._chunks = chunks

    def __iter__(self):
        return iter(self._chunks)


def test_write_stream_with_colors_win_color_and_noncolor_chunks(tmp_path):
    # Prepare a stream with a color chunk and a non-color chunk
    color_chunk = b'\x1b[31mRed Text\x1b[0m'
    noncolor_chunk = b'Plain text'
    stream = DummyStream([color_chunk, noncolor_chunk])

    # Create a temporary file and open it as a TextIOWrapper
    tmp_file = tmp_path / "output.txt"
    with open(tmp_file, "wb") as f:
        # Wrap the binary file with a TextIOWrapper to get .buffer
        text_out = io.TextIOWrapper(f, encoding="utf-8")
        write_stream_with_colors_win(stream, text_out, flush=False)

    # Read back the file content
    with open(tmp_file, "rb") as f:
        content = f.read()

    # The color chunk should have been decoded and written as text
    # The non-color chunk should have been written directly to the buffer
    expected = color_chunk + noncolor_chunk
    assert content == expected, "The output file content does not match expected bytes"


def test_write_stream_with_colors_win_flush_behavior(tmp_path):
    # Prepare a stream with a single non-color chunk
    chunk = b'Flush test'
    stream = DummyStream([chunk])

    # Create a temporary file and open it as a TextIOWrapper
    tmp_file = tmp_path / "flush_output.txt"
    with open(tmp_file, "wb") as f:
        text_out = io.TextIOWrapper(f, encoding="utf-8")
        # Capture the flush calls
        flush_calls = []

        original_flush = text_out.flush

        def counting_flush():
            flush_calls.append(True)
            original_flush()

        text_out.flush = counting_flush

        write_stream_with_colors_win(stream, text_out, flush=True)

    # After writing, the flush should have been called once
    assert len(flush_calls) == 1, "Flush was not called the expected number of times"

    # Verify that the file contains the chunk
    with open(tmp_file, "rb") as f:
        assert f.read() == chunk, "The chunk was not written correctly"


def test_write_stream_with_colors_win_encoding_handling(tmp_path):
    # Prepare a stream with a color chunk that contains non-ASCII characters
    # Use a UTF-8 encoded string with ANSI escape codes
    text = "こんにちは"  # Japanese greeting
    color_chunk = b'\x1b[32m' + text.encode("utf-8") + b'\x1b[0m'
    stream = DummyStream([color_chunk])

    # Create a temporary file with a specific encoding (utf-8)
    tmp_file = tmp_path / "encoding_output.txt"
    with open(tmp_file, "wb") as f:
        text_out = io.TextIOWrapper(f, encoding="utf-8")
        write_stream_with_colors_win(stream, text_out, flush=False)

    # Read back the file content as bytes
    with open(tmp_file, "rb") as f:
        content = f.read()

    # The color chunk should have been decoded and written as text,
    # resulting in the same bytes as the original chunk
    assert content == color_chunk, "Encoding handling failed: output bytes differ from input"
