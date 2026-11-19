import ssl
import pytest
from tornado.netutil import ssl_options_to_context

def test_ssl_options_to_context_returns_same_context():
    """Passing an existing SSLContext should return the same object."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    result = ssl_options_to_context(ctx)
    assert result is ctx

def test_ssl_options_to_context_dict_protocol_and_verify():
    """Dictionary options should create a context with the requested protocol and verify mode."""
    opts = {
        "ssl_version": ssl.PROTOCOL_TLSv1_2,
        "cert_reqs": ssl.CERT_REQUIRED,
        "ciphers": "ECDHE-RSA-AES128-GCM-SHA256",
    }
    ctx = ssl_options_to_context(opts, server_side=False)
    # Protocol should be TLSv1.2
    assert ctx.protocol == ssl.PROTOCOL_TLSv1_2
    # Verify mode should be CERT_REQUIRED
    assert ctx.verify_mode == ssl.CERT_REQUIRED
    # Cipher list should contain the specified cipher
    assert "ECDHE-RSA-AES128-GCM-SHA256" in ctx.get_ciphers()[0]["name"]

def test_ssl_options_to_context_invalid_keys_and_type():
    """Invalid input types or keys should raise an AssertionError."""
    # Non-dict input that is not an SSLContext
    with pytest.raises(AssertionError):
        ssl_options_to_context(123)

    # Dict with an invalid key
    with pytest.raises(AssertionError):
        ssl_options_to_context({"invalid_key": "value"})
