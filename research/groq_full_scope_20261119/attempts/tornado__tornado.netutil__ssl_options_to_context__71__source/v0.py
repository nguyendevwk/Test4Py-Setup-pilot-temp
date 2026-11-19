import ssl
import pytest
from tornado.netutil import ssl_options_to_context

def test_ssl_options_to_context_returns_same_context():
    """Passing an existing SSLContext should return the same object."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    result = ssl_options_to_context(ctx)
    assert result is ctx
    # Ensure that the context is still configured as client
    assert result.verify_mode == ssl.CERT_REQUIRED

def test_ssl_options_to_context_dict_server_side_and_client():
    """Dictionary options are converted correctly for server and client."""
    # Server side context
    server_opts = {"ssl_version": ssl.PROTOCOL_TLS_SERVER, "cert_reqs": ssl.CERT_NONE}
    server_ctx = ssl_options_to_context(server_opts, server_side=True)
    assert server_ctx.protocol == ssl.PROTOCOL_TLS_SERVER
    assert server_ctx.verify_mode == ssl.CERT_NONE
    assert server_ctx.check_hostname is False

    # Client side context
    client_opts = {"ssl_version": ssl.PROTOCOL_TLS_CLIENT, "cert_reqs": ssl.CERT_REQUIRED}
    client_ctx = ssl_options_to_context(client_opts, server_side=False)
    assert client_ctx.protocol == ssl.PROTOCOL_TLS_CLIENT
    assert client_ctx.verify_mode == ssl.CERT_REQUIRED
    assert client_ctx.check_hostname is True

def test_ssl_options_to_context_invalid_key_raises():
    """Providing an unknown keyword raises an AssertionError."""
    bad_opts = {"unknown_key": 123}
    with pytest.raises(AssertionError) as excinfo:
        ssl_options_to_context(bad_opts)
    assert "unknown_key" in str(excinfo.value)
