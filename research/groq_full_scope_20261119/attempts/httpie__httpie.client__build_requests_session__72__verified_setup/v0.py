import pytest
import requests
from httpie.client import build_requests_session
from httpie.ssl_ import AVAILABLE_SSL_VERSION_ARG_MAPPING, HTTPieHTTPSAdapter
from httpie.adapters import HTTPieHTTPAdapter
from httpie.plugins.registry import plugin_manager


def test_session_mounts_http_and_https_adapters(monkeypatch):
    """The returned session should have the HTTPie adapters mounted for http:// and https://."""
    # Ensure no plugin adapters interfere
    monkeypatch.setattr(plugin_manager, "get_transport_plugins", lambda: [])
    session = build_requests_session(verify=True)
    # The adapters should be instances of the expected classes
    assert isinstance(session.adapters["http://"], HTTPieHTTPAdapter)
    assert isinstance(session.adapters["https://"], HTTPieHTTPSAdapter)
    # The HTTPS adapter should have verify set to True
    https_adapter = session.adapters["https://"]
    assert https_adapter.verify is True
    # The HTTPS adapter should have no ssl_version when None is passed
    assert https_adapter.ssl_version is None


def test_ssl_version_mapping(monkeypatch):
    """Passing an ssl_version string should map to the correct ssl_version constant."""
    # Pick a known mapping key
    key = next(iter(AVAILABLE_SSL_VERSION_ARG_MAPPING))
    expected_ssl_version = AVAILABLE_SSL_VERSION_ARG_MAPPING[key]
    # Ensure no plugin adapters interfere
    monkeypatch.setattr(plugin_manager, "get_transport_plugins", lambda: [])
    session = build_requests_session(verify=False, ssl_version=key)
    https_adapter = session.adapters["https://"]
    # The adapter should have the mapped ssl_version
    assert https_adapter.ssl_version == expected_ssl_version
    # Verify that verify flag is respected
    assert https_adapter.verify is False


def test_invalid_ssl_version_raises_key_error(monkeypatch):
    """Providing an unknown ssl_version string should raise a KeyError during adapter creation."""
    # Ensure no plugin adapters interfere
    monkeypatch.setattr(plugin_manager, "get_transport_plugins", lambda: [])
    with pytest.raises(KeyError):
        build_requests_session(verify=True, ssl_version="nonexistent_ssl_version")
