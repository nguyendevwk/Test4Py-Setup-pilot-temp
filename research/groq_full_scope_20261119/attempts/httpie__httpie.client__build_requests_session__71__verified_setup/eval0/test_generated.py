import pytest
import requests
from httpie.client import build_requests_session
from httpie.adapters import HTTPieHTTPAdapter, HTTPieHTTPSAdapter
from httpie.plugins.registry import plugin_manager


def test_build_session_default_adapters():
    """Verify that the default HTTP and HTTPS adapters are mounted."""
    session = build_requests_session(verify=True)
    # The session should have our custom adapters for http:// and https://
    http_adapter = session.adapters.get('http://')
    https_adapter = session.adapters.get('https://')
    assert isinstance(http_adapter, HTTPieHTTPAdapter)
    assert isinstance(https_adapter, HTTPieHTTPSAdapter)
    # The HTTPS adapter should be configured with verify=True
    assert https_adapter.verify is True
    # No ciphers or ssl_version should be set
    assert https_adapter.ciphers is None
    assert https_adapter.ssl_version is None


def test_build_session_with_ssl_and_ciphers(monkeypatch):
    """Verify that passing ssl_version and ciphers correctly configures the HTTPS adapter."""
    # Use a known SSL version key from AVAILABLE_SSL_VERSION_ARG_MAPPING
    from httpie.ssl_ import AVAILABLE_SSL_VERSION_ARG_MAPPING
    ssl_key = next(iter(AVAILABLE_SSL_VERSION_ARG_MAPPING))
    session = build_requests_session(verify=False, ssl_version=ssl_key, ciphers="ECDHE-RSA-AES128-GCM-SHA256")
    https_adapter = session.adapters.get('https://')
    assert isinstance(https_adapter, HTTPieHTTPSAdapter)
    # The adapter should have the mapped ssl_version value
    expected_ssl_version = AVAILABLE_SSL_VERSION_ARG_MAPPING[ssl_key]
    assert https_adapter.ssl_version == expected_ssl_version
    # The adapter should have the ciphers string we passed
    assert https_adapter.ciphers == "ECDHE-RSA-AES128-GCM-SHA256"
    # Verify flag should be False
    assert https_adapter.verify is False


def test_build_session_with_plugins(monkeypatch):
    """Verify that transport plugins are mounted on the session."""
    # Create a dummy plugin class with required attributes
    class DummyPlugin:
        prefix = "ftp://"
        def get_adapter(self):
            return requests.adapters.HTTPAdapter()

    # Monkeypatch the plugin manager to return our dummy plugin
    monkeypatch.setattr(plugin_manager, "get_transport_plugins", lambda: [DummyPlugin])
    session = build_requests_session(verify=True)
    # The dummy plugin's adapter should be mounted under its prefix
    ftp_adapter = session.adapters.get("ftp://")
    assert ftp_adapter is not None
    assert isinstance(ftp_adapter, requests.adapters.HTTPAdapter)
