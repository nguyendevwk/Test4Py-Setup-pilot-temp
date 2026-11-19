import pytest
from httpie.output.writer import write_raw_data
from httpie.output.writer import write_message
from httpie.context import Environment
from httpie.models import OutputOptions
from httpie.cli.dicts import HTTPHeadersDict
from httpie.output.processing import ProcessingOptions


def test_write_raw_data_defaults(monkeypatch):
    captured = {}

    def fake_write_message(requests_message, env, output_options, processing_options, extra_stream_kwargs):
        captured.update({
            "requests_message": requests_message,
            "env": env,
            "output_options": output_options,
            "processing_options": processing_options,
            "extra_stream_kwargs": extra_stream_kwargs,
        })
        return "sentinel"

    monkeypatch.setattr(write_message, "__call__", fake_write_message)

    env = Environment()
    data = b"hello world"

    result = write_raw_data(env, data)

    assert result == "sentinel"
    assert isinstance(captured["processing_options"], ProcessingOptions)
    assert captured["extra_stream_kwargs"] is None
    assert isinstance(captured["output_options"], OutputOptions)
    assert captured["output_options"].body is True
    assert captured["output_options"].headers is False
    assert captured["requests_message"].body == data
    assert isinstance(captured["requests_message"].headers, HTTPHeadersDict)


def test_write_raw_data_with_custom_headers(monkeypatch):
    captured = {}

    def fake_write_message(requests_message, env, output_options, processing_options, extra_stream_kwargs):
        captured.update({
            "requests_message": requests_message,
            "env": env,
            "output_options": output_options,
            "processing_options": processing_options,
            "extra_stream_kwargs": extra_stream_kwargs,
        })
        return "sentinel"

    monkeypatch.setattr(write_message, "__call__", fake_write_message)

    env = Environment()
    data = b"foo bar"
    headers = HTTPHeadersDict({"Content-Type": "text/plain"})

    result = write_raw_data(env, data, headers=headers)

    assert result == "sentinel"
    assert captured["requests_message"].headers["Content-Type"] == "text/plain"
    assert captured["requests_message"].body == data


def test_write_raw_data_with_stream_kwargs(monkeypatch):
    captured = {}

    def fake_write_message(requests_message, env, output_options, processing_options, extra_stream_kwargs):
        captured.update({
            "requests_message": requests_message,
            "env": env,
            "output_options": output_options,
            "processing_options": processing_options,
            "extra_stream_kwargs": extra_stream_kwargs,
        })
        return "sentinel"

    monkeypatch.setattr(write_message, "__call__", fake_write_message)

    env = Environment()
    data = b"baz"
    stream_kwargs = {"encoding": "utf-8"}

    result = write_raw_data(env, data, stream_kwargs=stream_kwargs)

    assert result == "sentinel"
    assert captured["extra_stream_kwargs"] == stream_kwargs
