import pytest
import requests
from httpie.client import build_requests_session
from httpie.adapters import HTTPieHTTPAdapter, HTTPieHTTPSAdapter
from httpie.ssl_ import AVAILABLE_SSL_VERSION_ARG_MAPPING

def test_build_requests_session_default_adapters(monkeypatch):
    # Ensure that the default session mounts the correct adapters for http and https
    session = build_requests_session(verify=True)
    # The adapters should be instances of the custom classes
    assert isinstance(session.adapters['http://'], HTTPieHTTPAdapter)
    assert isinstance(session.adapters['https://'], HTTPieHTTPSAdapter)
    # The HTTPS adapter should have verify=True and no specific ssl_version
    https_adapter = session.adapters['https://']
    assert https_adapter.verify is True
    assert https_adapter.ssl_version is None

def test_build_requests_session_with_ssl_and_ciphers(monkeypatch):
    # Use a specific SSL version and cipher suite
    ssl_version = 'TLSv1_2'
    ciphers = 'ECDHE'
    session = build_requests_session(verify=False, ssl_version=ssl_version, ciphers=ciphers)
    https_adapter = session.adapters['https://']
    # Verify that the adapter was configured with the correct SSL version mapping
    expected_ssl_version = AVAILABLE_SSL_VERSION_ARG_MAPPING[ssl_version]
    assert https_adapter.ssl_version == expected_ssl_version
    # Verify that the cipher suite was passed through
    assert https_adapter.ciphers == ciphers
    # Verify that verify flag is respected
    assert https_adapter.verify is False

def test_build_requests_session_invalid_ssl_version(monkeypatch):
    # Passing an unknown ssl_version should raise a KeyError during mapping
    with pytest.raises(KeyError):
        build_requests_session(verify=True, ssl_version='UNKNOWN_SSL_VERSION')
