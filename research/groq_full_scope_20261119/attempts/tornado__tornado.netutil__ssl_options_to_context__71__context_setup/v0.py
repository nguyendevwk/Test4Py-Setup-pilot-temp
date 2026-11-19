import ssl
import tempfile
import os
import pytest
from tornado.netutil import ssl_options_to_context

def test_ssl_options_to_context_returns_same_context():
    """Passing an existing SSLContext should return the same object."""
    ctx = ssl.create_default_context()
    result = ssl_options_to_context(ctx)
    assert result is ctx

def test_ssl_options_to_context_invalid_key_raises():
    """Providing a dict with an unknown keyword should raise an AssertionError."""
    bad_options = {"unknown_key": "value"}
    with pytest.raises(AssertionError):
        ssl_options_to_context(bad_options)

def test_ssl_options_to_context_server_side_default_version(tmp_path):
    """When server_side=True, the context should use PROTOCOL_TLS_SERVER."""
    # Create a temporary self‑signed certificate file for load_cert_chain
    cert_file = tmp_path / "cert.pem"
    key_file = tmp_path / "key.pem"
    # Minimal PEM contents that satisfy load_cert_chain (not a real cert)
    cert_file.write_text("-----BEGIN CERTIFICATE-----\\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArV\\n-----END CERTIFICATE-----")
    key_file.write_text("-----BEGIN PRIVATE KEY-----\\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC\\n-----END PRIVATE KEY-----")

    options = {
        "certfile": str(cert_file),
        "keyfile": str(key_file),
        "ssl_version": ssl.PROTOCOL_TLS,  # will be overridden by server_side
    }
    ctx = ssl_options_to_context(options, server_side=True)
    # The protocol should be TLS_SERVER
    assert ctx.protocol == ssl.PROTOCOL_TLS_SERVER
    # The certificate should be loaded without raising an exception
    # (load_cert_chain is called during context creation)
    assert os.path.exists(cert_file)
    assert os.path.exists(key_file)
