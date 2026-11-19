import re
import types
import pytest
from httpie.output.processing import Formatting, is_valid_mime, MIME_RE

# Helper to create a dummy plugin class
def make_plugin(name, enabled=True, modify_headers=None, modify_body=None, modify_metadata=None):
    class DummyPlugin:
        def __init__(self, env=None, **kwargs):
            self.enabled = enabled
        def format_headers(self, headers):
            return modify_headers(headers) if modify_headers else headers
        def format_body(self, content, mime):
            return modify_body(content, mime) if modify_body else content
        def format_metadata(self, metadata):
            return modify_metadata(metadata) if modify_metadata else metadata
    DummyPlugin.__name__ = name
    return DummyPlugin

@pytest.fixture(autouse=True)
def patch_plugin_manager(monkeypatch):
    """Patch plugin_manager to return controlled dummy plugins."""
    dummy_group = {
        "dummy": [
            make_plugin("HeaderUpper", enabled=True,
                        modify_headers=lambda h: h.upper()),
            make_plugin("BodyAdd", enabled=True,
                        modify_body=lambda c, m: c + "!!!"),
            make_plugin("MetaStrip", enabled=True,
                        modify_metadata=lambda m: m.strip()),
        ]
    }
    dummy_manager = types.SimpleNamespace(
        get_formatters_grouped=lambda: dummy_group
    )
    monkeypatch.setattr("httpie.output.processing.plugin_manager", dummy_manager)

def test_formatting_no_plugins(monkeypatch):
    """When no groups are requested, formatting methods return input unchanged."""
    # Patch plugin_manager to return empty groups
    monkeypatch.setattr("httpie.output.processing.plugin_manager",
                        types.SimpleNamespace(get_formatters_grouped=lambda: {}))
    fmt = Formatting(groups=[])
    assert fmt.format_headers("Content-Type: text/plain") == "Content-Type: text/plain"
    assert fmt.format_body("body", "text/plain") == "body"
    assert fmt.format_metadata("  meta  ") == "  meta  "

def test_formatting_header_and_metadata(monkeypatch):
    """Header and metadata are processed by enabled plugins."""
    fmt = Formatting(groups=["dummy"])
    headers = "content-type: text/plain"
    metadata = "  meta data  "
    assert fmt.format_headers(headers) == headers.upper()
    assert fmt.format_metadata(metadata) == metadata.strip()

def test_formatting_body_mime_validation(monkeypatch):
    """Body is only processed when MIME is valid; invalid MIME leaves body unchanged."""
    fmt = Formatting(groups=["dummy"])
    body = "content"
    valid_mime = "text/plain"
    invalid_mime = "invalid-mime"
    # Valid MIME: body gets appended
    assert fmt.format_body(body, valid_mime) == body + "!!!"
    # Invalid MIME: body unchanged
    assert fmt.format_body(body, invalid_mime) == body
