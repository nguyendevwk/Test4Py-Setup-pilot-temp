import pytest
from httpie.output.processing import Formatting
from httpie.plugins.registry import plugin_manager
from httpie.context import Environment

# Helper plugin that records calls and optionally raises
class DummyPlugin:
    def __init__(self, env=Environment(), **kwargs):
        self.enabled = True
        self.calls = []

    def format_headers(self, headers: str) -> str:
        self.calls.append(("headers", headers))
        return f"hdr:{headers}"

    def format_body(self, content: str, mime: str) -> str:
        self.calls.append(("body", content, mime))
        return f"body:{content}"

    def format_metadata(self, metadata: str) -> str:
        self.calls.append(("metadata", metadata))
        return f"meta:{metadata}"


def test_formatting_applies_all_plugins(monkeypatch):
    # Monkeypatch plugin_manager to return our dummy plugin in a group
    monkeypatch.setattr(
        plugin_manager,
        "get_formatters_grouped",
        lambda: {"default": [DummyPlugin]},
    )
    fmt = Formatting(groups=["default"])
    # All three formatting methods should be applied
    hdr = fmt.format_headers("Content-Type: application/json")
    assert hdr == "hdr:Content-Type: application/json"
    body = fmt.format_body("{}", "application/json")
    assert body == "body:{}"
    meta = fmt.format_metadata("some meta")
    assert meta == "meta:some meta"


def test_formatting_skips_body_when_mime_invalid(monkeypatch):
    # Dummy plugin that would modify body if called
    monkeypatch.setattr(
        plugin_manager,
        "get_formatters_grouped",
        lambda: {"default": [DummyPlugin]},
    )
    fmt = Formatting(groups=["default"])
    # Use an invalid mime type; body should remain unchanged
    body = fmt.format_body("{}", "invalid/mime")
    assert body == "{}"


def test_formatting_raises_when_plugin_fails(monkeypatch):
    # Plugin that raises an exception during header formatting
    class FailingPlugin:
        def __init__(self, env=Environment(), **kwargs):
            self.enabled = True

        def format_headers(self, headers: str) -> str:
            raise RuntimeError("plugin failure")

        def format_body(self, content: str, mime: str) -> str:
            return content

        def format_metadata(self, metadata: str) -> str:
            return metadata

    monkeypatch.setattr(
        plugin_manager,
        "get_formatters_grouped",
        lambda: {"default": [FailingPlugin]},
    )
    fmt = Formatting(groups=["default"])
    with pytest.raises(RuntimeError, match="plugin failure"):
        fmt.format_headers("Content-Type: text/plain")
