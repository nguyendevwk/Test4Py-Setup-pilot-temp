import re
import types
import pytest

# Import the target class
from httpie.output.processing import Formatting

# Helper dummy plugin that records calls and modifies data
class DummyPlugin:
    def __init__(self, env=None, **kwargs):
        self.enabled = True
        self.env = env
        self.kwargs = kwargs
        self.calls = []

    def format_headers(self, headers: str) -> str:
        self.calls.append(("headers", headers))
        return headers + " [dummy-headers]"

    def format_body(self, content: str, mime: str) -> str:
        self.calls.append(("body", content, mime))
        return content + f" [dummy-body:{mime}]"

    def format_metadata(self, metadata: str) -> str:
        self.calls.append(("metadata", metadata))
        return metadata + " [dummy-metadata]"

# Test normal behavior: all plugins applied in order
def test_formatting_applies_plugins(monkeypatch):
    # Monkeypatch plugin_manager to return our dummy plugin
    dummy_manager = types.SimpleNamespace(
        get_formatters_grouped=lambda: {"default": [DummyPlugin]}
    )
    monkeypatch.setattr("httpie.output.processing.plugin_manager", dummy_manager)

    fmt = Formatting(groups=["default"])
    # Ensure plugin is enabled
    assert len(fmt.enabled_plugins) == 1
    plugin = fmt.enabled_plugins[0]
    assert isinstance(plugin, DummyPlugin)

    # Test header formatting
    hdr = fmt.format_headers("Content-Type: application/json")
    assert hdr.endswith("[dummy-headers]")
    assert plugin.calls[0][0] == "headers"

    # Test body formatting with valid mime
    body = fmt.format_body("{}", "application/json")
    assert body.endswith("[dummy-body:application/json]")
    assert plugin.calls[1][0] == "body"

    # Test metadata formatting
    meta = fmt.format_metadata("meta")
    assert meta.endswith("[dummy-metadata]")
    assert plugin.calls[2][0] == "metadata"

# Test boundary: no plugins enabled
def test_formatting_no_plugins(monkeypatch):
    # Return empty group list
    dummy_manager = types.SimpleNamespace(
        get_formatters_grouped=lambda: {"empty": []}
    )
    monkeypatch.setattr("httpie.output.processing.plugin_manager", dummy_manager)

    fmt = Formatting(groups=["empty"])
    assert fmt.enabled_plugins == []

    # Formatting should return input unchanged
    assert fmt.format_headers("X-Test: 1") == "X-Test: 1"
    assert fmt.format_body("data", "text/plain") == "data"
    assert fmt.format_metadata("meta") == "meta"

# Test error: invalid MIME type skips body formatting
def test_formatting_invalid_mime(monkeypatch):
    # Dummy plugin that would modify body if called
    dummy_manager = types.SimpleNamespace(
        get_formatters_grouped=lambda: {"default": [DummyPlugin]}
    )
    monkeypatch.setattr("httpie.output.processing.plugin_manager", dummy_manager)

    # Monkeypatch is_valid_mime to always return False
    monkeypatch.setattr("httpie.output.processing.is_valid_mime", lambda m: False)

    fmt = Formatting(groups=["default"])
    plugin = fmt.enabled_plugins[0]

    # Body should remain unchanged because mime is invalid
    body = fmt.format_body("{}", "invalid/mime")
    assert body == "{}"
    # Plugin should not have been called for body
    assert all(call[0] != "body" for call in plugin.calls)
