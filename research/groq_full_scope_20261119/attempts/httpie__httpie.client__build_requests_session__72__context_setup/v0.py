import pytest
import requests
from httpie.client import build_requests_session
from httpie.plugins.registry import plugin_manager
from httpie.adapters import HTTPieHTTPSAdapter


def test_build_requests_session_mounts_http_and_https_adapters():
    """The session should mount HTTPieHTTPAdapter for http:// and HTTPieHTTPSAdapter for https://."""
    session = build_requests_session(verify=True)
    # The adapters dict keys are the prefixes used for mounting
    assert "http://" in session.adapters
    assert "https://" in session.adapters
    # The http adapter should be an instance of HTTPieHTTPAdapter
    assert isinstance(session.adapters["http://"], type(session.adapters["http://"]))
    # The https adapter should be an instance of HTTPieHTTPSAdapter
    assert isinstance(session.adapters["https://"], HTTPieHTTPSAdapter)


def test_build_requests_session_ssl_version_and_ciphers(monkeypatch):
    """Verify that ssl_version and ciphers are forwarded to HTTPieHTTPSAdapter."""
    # Create a dummy adapter class to capture init arguments
    captured = {}
    class DummyHTTPSAdapter(HTTPieHTTPSAdapter):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            captured.update(kwargs)

    # Monkeypatch the HTTPS adapter used in build_requests_session
    monkeypatch.setattr(
        "httpie.client.HTTPieHTTPSAdapter",
        DummyHTTPSAdapter,
    )

    # Call with specific ssl_version and ciphers
    session = build_requests_session(verify=False, ssl_version="TLSv1_2", ciphers="ECDHE-RSA-AES128-GCM-SHA256")

    # The captured kwargs should contain the forwarded values
    assert captured["verify"] is False
    assert captured["ssl_version"] == "TLSv1_2"
    assert captured["ciphers"] == "ECDHE-RSA-AES128-GCM-SHA256"

    # The session should still have the https adapter mounted
    assert "https://" in session.adapters
    assert isinstance(session.adapters["https://"], DummyHTTPSAdapter)


def test_build_requests_session_mounts_plugin_adapters(monkeypatch):
    """Plugins should be able to mount additional adapters via the plugin manager."""
    # Define a dummy plugin with a unique prefix and adapter
    class DummyPlugin:
        prefix = "ftp://"

        def get_adapter(self):
            return requests.adapters.HTTPAdapter()

    # Monkeypatch the plugin manager to return our dummy plugin
    monkeypatch.setattr(
        plugin_manager,
        "get_transport_plugins",
        lambda: [DummyPlugin],
    )

    session = build_requests_session(verify=True)

    # The dummy plugin's adapter should be mounted under its prefix
    assert "ftp://" in session.adapters
    assert isinstance(session.adapters["ftp://"], requests.adapters.HTTPAdapter)
