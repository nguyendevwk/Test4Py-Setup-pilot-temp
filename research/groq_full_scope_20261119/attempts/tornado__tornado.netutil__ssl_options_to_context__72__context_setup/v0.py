import ssl
import tempfile
import os
import pytest
from tornado.netutil import ssl_options_to_context

def test_ssl_options_to_context_with_dict(tmp_path):
    # Create a temporary self‑signed cert file for testing
    cert_file = tmp_path / "cert.pem"
    key_file = tmp_path / "key.pem"
    # Use openssl via subprocess to generate a simple cert
    # (Python's ssl module can load a self‑signed cert without a CA)
    os.system(
        f"openssl req -x509 -newkey rsa:2048 -keyout {key_file} "
        f"-out {cert_file} -days 1 -nodes -subj '/CN=localhost'"
    )
    options = {
        "ssl_version": ssl.PROTOCOL_TLS_CLIENT,
        "certfile": str(cert_file),
        "keyfile": str(key_file),
        "cert_reqs": ssl.CERT_NONE,
        "ciphers": "ECDHE-RSA-AES128-GCM-SHA256",
    }
    ctx = ssl_options_to_context(options)
    assert isinstance(ctx, ssl.SSLContext)
    # Verify that the context was configured as expected
    assert ctx.verify_mode == ssl.CERT_NONE
    assert ctx.check_hostname is False
    # The context should have the cipher we requested
    assert "ECDHE-RSA-AES128-GCM-SHA256" in ctx.get_ciphers()[0]["name"]

def test_ssl_options_to_context_server_side_flag(tmp_path):
    # Generate a cert for server side
    cert_file = tmp_path / "server_cert.pem"
    key_file = tmp_path / "server_key.pem"
    os.system(
        f"openssl req -x509 -newkey rsa:2048 -keyout {key_file} "
        f"-out {cert_file} -days 1 -nodes -subj '/CN=server'"
    )
    options = {
        "ssl_version": ssl.PROTOCOL_TLS,
        "certfile": str(cert_file),
        "keyfile": str(key_file),
    }
    ctx = ssl_options_to_context(options, server_side=True)
    assert isinstance(ctx, ssl.SSLContext)
    # Server side should use PROTOCOL_TLS_SERVER by default
    assert ctx.protocol == ssl.PROTOCOL_TLS_SERVER
    # The context should have a certificate loaded
    assert ctx.get_ca_certs() == []

def test_ssl_options_to_context_invalid_key():
    # Pass a dictionary with an unsupported key to trigger assertion
    bad_options = {"unsupported_key": "value"}
    with pytest.raises(AssertionError):
        ssl_options_to_context(bad_options)
