import importlib
import types
import requests
import pytest

# Import the target function
from httpie.client import build_requests_session
# Import plugin manager to monkeypatch
from httpie.plugins.registry import plugin_manager

def test_session_mounts_http_and_https_adapters():
    """
    Verify that the returned session has the custom HTTPie adapters mounted
    for both http:// and https:// prefixes.
    """
    session = build_requests_session(verify=True)
    # The adapters should be instances of HTTPieHTTPAdapter and HTTPieHTTPSAdapter
    http_adapter = session.adapters.get('http://')
    https_adapter = session.adapters.get('https://')
    assert http_adapter is not None, "HTTP adapter not mounted"
    assert https_adapter is not None, "HTTPS adapter not mounted"
    # Ensure they are of the expected types
    from httpie.adapters import HTTPieHTTPAdapter, HTTPieHTTPSAdapter
    assert isinstance(http_adapter, HTTPieHTTPAdapter), "Incorrect HTTP adapter type"
    assert isinstance(https_adapter, HTTPieHTTPSAdapter), "Incorrect HTTPS adapter type"

def test_session_mounts_plugin_adapters(monkeypatch):
    """
    Verify that plugin transport adapters are mounted on the session.
    A dummy plugin is created and registered via monkeypatching the plugin manager.
    """
    # Create a dummy plugin class
    class DummyPlugin:
        prefix = 'ftp://'
        def get_adapter(self):
            return requests.adapters.HTTPAdapter()
    # Monkeypatch the plugin manager to return our dummy plugin
    monkeypatch.setattr(plugin_manager, "get_transport_plugins", lambda: [DummyPlugin])
    session = build_requests_session(verify=False)
    # The dummy plugin adapter should be mounted under its prefix
    ftp_adapter = session.adapters.get('ftp://')
    assert ftp_adapter is not None, "Plugin adapter not mounted"
    assert isinstance(ftp_adapter, requests.adapters.HTTPAdapter), "Incorrect plugin adapter type"

def test_build_requests_session_verify_and_ssl_version():
    """
    Verify that the HTTPS adapter is configured with the correct verify flag
    and ssl_version mapping when provided.
    """
    # Use a known ssl_version key from AVAILABLE_SSL_VERSION_ARG_MAPPING
    from httpie.ssl_ import AVAILABLE_SSL_VERSION_ARG_MAPPING
    ssl_key = next(iter(AVAILABLE_SSL_VERSION_ARG_MAPPING))
    session = build_requests_session(verify=False, ssl_version=ssl_key)
    https_adapter = session.adapters.get('https://')
    # The adapter should have the verify attribute set to False
    assert hasattr(https_adapter, "verify")
    assert https_adapter.verify is False
    # The ssl_version attribute should be set to the mapped value
    expected_ssl_version = AVAILABLE_SSL_VERSION_ARG_MAPPING[ssl_key]
    assert getattr(https_adapter, "ssl_version", None) == expected_ssl_version
