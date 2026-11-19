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

def test_ssl_options_to_context_dict_cert_reqs_none():
    """When cert_reqs is CERT_NONE, the context should have check_hostname False."""
    options = {"cert_reqs": ssl.CERT_NONE}
    ctx = ssl_options_to_context(options)
    assert ctx.verify_mode == ssl.CERT_NONE
    assert ctx.check_hostname is False

def test_ssl_options_to_context_server_side_sets_server_protocol(tmp_path):
    """server_side=True should set the protocol to TLS_SERVER."""
    # Create a minimal valid cert file using a temporary file
    cert_file = tmp_path / "cert.pem"
    cert_file.write_text("-----BEGIN CERTIFICATE-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArV\n-----END CERTIFICATE-----")
    key_file = tmp_path / "key.pem"
    key_file.write_text("-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASC...\n-----END PRIVATE KEY-----")
    options = {
        "certfile": str(cert_file),
        "keyfile": str(key_file),
        "server_side": True,
    }
    ctx = ssl_options_to_context(options)
    # The protocol should be TLS_SERVER
    assert ctx.protocol == ssl.PROTOCOL_TLS_SERVER
    # The context should have a certificate loaded (no exception on getpeercert)
    # Since we didn't actually create a valid cert, just ensure no exception on load
    # The load_cert_chain call will raise if cert is invalid, so reaching here means success
    assert isinstance(ctx, ssl.SSLContext)
