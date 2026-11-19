import pytest
from httpie.output.writer import get_stream_type_and_kwargs
from httpie.output.streams import RawStream, EncodedStream, PrettyStream, BufferedPrettyStream
from httpie.models import HTTPResponse
from httpie.output.processing import Conversion, Formatting
from httpie.output.processing import ProcessingOptions
from httpie.context import Environment
from httpie.cli.dicts import HTTPHeadersDict


class DummyEnv(Environment):
    def __init__(self, stdout_isatty: bool):
        self.stdout_isatty = stdout_isatty


def test_raw_stream_non_tty_no_prettify():
    env = DummyEnv(stdout_isatty=False)
    proc_opts = ProcessingOptions(stream=False, style=None, json=False, format_options=None,
                                  response_mime=None, response_charset=None)
    headers = HTTPHeadersDict()
    stream_cls, kwargs = get_stream_type_and_kwargs(env, proc_opts, HTTPResponse, headers)
    assert stream_cls is RawStream
    assert kwargs["chunk_size"] == RawStream.CHUNK_SIZE


def test_pretty_stream_tty_with_prettify():
    env = DummyEnv(stdout_isatty=True)
    proc_opts = ProcessingOptions(stream=False, style="monokai", json=True,
                                  format_options={"indent": 2},
                                  response_mime="application/json",
                                  response_charset="utf-8")
    headers = HTTPHeadersDict()
    stream_cls, kwargs = get_stream_type_and_kwargs(env, proc_opts, HTTPResponse, headers)
    assert stream_cls is BufferedPrettyStream
    assert isinstance(kwargs["conversion"], Conversion)
    assert isinstance(kwargs["formatting"], Formatting)
    assert kwargs["formatting"].color_scheme == "monokai"
    assert kwargs["formatting"].explicit_json is True
    assert kwargs["formatting"].format_options == {"indent": 2}
    assert kwargs["mime_overwrite"] == "application/json"
    assert kwargs["encoding_overwrite"] == "utf-8"


def test_auto_streaming_event_stream_header():
    env = DummyEnv(stdout_isatty=False)
    proc_opts = ProcessingOptions(stream=False, style=None, json=False, format_options=None,
                                  response_mime=None, response_charset=None)
    headers = HTTPHeadersDict({"Content-Type": "text/event-stream; charset=utf-8"})
    stream_cls, kwargs = get_stream_type_and_kwargs(env, proc_opts, HTTPResponse, headers)
    assert stream_cls is RawStream
    assert kwargs["chunk_size"] == RawStream.CHUNK_SIZE_BY_LINE
