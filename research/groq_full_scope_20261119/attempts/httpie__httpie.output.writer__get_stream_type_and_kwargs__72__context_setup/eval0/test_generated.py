import pytest
from httpie.output.writer import get_stream_type_and_kwargs
from httpie.output.streams import (
    RawStream, EncodedStream, PrettyStream, BufferedPrettyStream
)
from httpie.models import HTTPResponse, HTTPMessage
from httpie.cli.dicts import HTTPHeadersDict


class DummyEnv:
    def __init__(self, stdout_isatty: bool):
        self.stdout_isatty = stdout_isatty
        self.encoding = "utf-8"
        self.color_scheme = "default"


class DummyProcessingOptions:
    def __init__(
        self,
        stream: bool = False,
        prettify_groups=None,
        response_mime=None,
        response_charset=None,
        style=None,
        json=False,
        format_options=None,
    ):
        self.stream = stream
        self._prettify_groups = prettify_groups or []
        self.response_mime = response_mime
        self.response_charset = response_charset
        self.style = style
        self.json = json
        self.format_options = format_options or {}

    def get_prettify(self, env):
        return self._prettify_groups


def test_raw_stream_non_tty_event_stream():
    env = DummyEnv(stdout_isatty=False)
    opts = DummyProcessingOptions(stream=False)
    headers = HTTPHeadersDict({"Content-Type": "text/event-stream"})
    stream_cls, kwargs = get_stream_type_and_kwargs(
        env, opts, HTTPResponse, headers
    )
    assert stream_cls is RawStream
    assert kwargs["chunk_size"] == RawStream.CHUNK_SIZE_BY_LINE


def test_pretty_stream_tty_with_prettify():
    env = DummyEnv(stdout_isatty=True)
    opts = DummyProcessingOptions(
        stream=False,
        prettify_groups=["json"],
        response_mime="application/json",
        response_charset="utf-8",
        style="monokai",
        json=True,
        format_options={"indent": 2},
    )
    headers = HTTPHeadersDict()
    stream_cls, kwargs = get_stream_type_and_kwargs(
        env, opts, HTTPResponse, headers
    )
    assert stream_cls is PrettyStream
    assert kwargs["env"] is env
    assert kwargs["mime_overwrite"] == "application/json"
    assert kwargs["encoding_overwrite"] == "utf-8"
    assert "conversion" in kwargs
    assert "formatting" in kwargs
    assert kwargs["formatting"].color_scheme == "monokai"
    assert kwargs["formatting"].explicit_json is True
    assert kwargs["formatting"].format_options["indent"] == 2


def test_raw_stream_non_tty_no_event_stream():
    env = DummyEnv(stdout_isatty=False)
    opts = DummyProcessingOptions(stream=False)
    headers = HTTPHeadersDict({"Content-Type": "application/json"})
    stream_cls, kwargs = get_stream_type_and_kwargs(
        env, opts, HTTPMessage, headers
    )
    assert stream_cls is RawStream
    assert kwargs["chunk_size"] == RawStream.CHUNK_SIZE
