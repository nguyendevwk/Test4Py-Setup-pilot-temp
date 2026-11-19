import io
import pytest
from httpie.output.writer import write_raw_data
from httpie.context import Environment
from httpie.models import HTTPResponse
from httpie.output.streams import RawStream

# Helper to create a minimal Environment with an in-memory stdout
def make_env():
    env = Environment()
    env.stdout = io.BytesIO()
    return env

def test_write_raw_data_with_string_and_headers():
    env = make_env()
    data = "Hello, world!"
    headers = {"Content-Type": "text/plain"}
    result = write_raw_data(env, data, headers=headers)

    # The result should be a RawStream instance
    assert isinstance(result, RawStream)

    # The environment's stdout should contain the raw data
    env.stdout.seek(0)
    output = env.stdout.read()
    assert output == data.encode("utf-8")

    # The headers should be set on the underlying PreparedRequest
    # We can inspect the message inside the RawStream
    # RawStream has a .message attribute
    assert result.message.body == data
    assert result.message.headers["Content-Type"] == "text/plain"

def test_write_raw_data_with_bytes_and_no_headers():
    env = make_env()
    data = b"\x00\x01\x02\x03"
    result = write_raw_data(env, data)

    assert isinstance(result, RawStream)
    env.stdout.seek(0)
    output = env.stdout.read()
    assert output == data

    # No headers should be present
    assert result.message.headers == {}

def test_write_raw_data_with_processing_options_and_stream_kwargs():
    env = make_env()
    data = "Test data"
    # Use a dummy processing option that does nothing
    from httpie.output.processing import ProcessingOptions
    processing_options = ProcessingOptions()
    stream_kwargs = {"encoding": "utf-8"}

    result = write_raw_data(
        env,
        data,
        processing_options=processing_options,
        stream_kwargs=stream_kwargs
    )

    assert isinstance(result, RawStream)
    env.stdout.seek(0)
    output = env.stdout.read()
    assert output == data.encode("utf-8")
    # The stream kwargs should be applied to the RawStream
    assert result.encoding == "utf-8"
