import pytest
import requests
from httpie.client import build_requests_session
from httpie.ssl_ import AVAILABLE_SSL_VERSION_ARG_MAPPING
from httpie.adapters import HTTPieHTTPSAdapter, HTTPieHTTPAdapter

def test_build_requests_session_mounts_adapters(monkeypatch):
    # Ensure plugin_manager returns no plugins for isolation
    monkeypatch.setattr(
        "httpie.client.plugin_manager.get_transport_plugins",
        lambda: [],
    )
    session = build_requests_session(verify=True, ssl_version="TLSv1_2", ciphers="DEFAULT")
    # Check that HTTP and HTTPS adapters are mounted
    assert "http://" in session.adapters
    assert "https://" in session.adapters
    http_adapter = session.adapters["http://"]
    https_adapter = session.adapters["https://"]
    assert isinstance(http_adapter, HTTPieHTTPAdapter)
    assert isinstance(https_adapter, HTTPieHTTPSAdapter)
    # Verify adapter configuration
    assert https_adapter.verify is True
    expected_ssl_version = AVAILABLE_SSL_VERSION_ARG_MAPPING["TLSv1_2"]
    assert https_adapter.ssl_version == expected_ssl_version
    assert https_adapter.ciphers == "DEFAULT"

def test_build_requests_session_without_ssl_version(monkeypatch):
    monkeypatch.setattr(
        "httpie.client.plugin_manager.get_transport_plugins",
        lambda: [],
    )
    session = build_requests_session(verify=False, ssl_version=None, ciphers=None)
    https_adapter = session.adapters["https://"]
    # When ssl_version is None, adapter should not set ssl_version
    assert isinstance(https_adapter, HTTPieHTTPSAdapter)
    assert https_adapter.ssl_version is None
    assert https_adapter.verify is False
    assert https_adapter.ciphers is None

def test_build_requests_session_invalid_ssl_version(monkeypatch):
    monkeypatch.setattr(
        "httpie.client.plugin_manager.get_transport_plugins",
        lambda: [],
    )
    with pytest.raises(KeyError):
        build_requests_session(verify=True, ssl_version="INVALID_VERSION", ciphers=None)
