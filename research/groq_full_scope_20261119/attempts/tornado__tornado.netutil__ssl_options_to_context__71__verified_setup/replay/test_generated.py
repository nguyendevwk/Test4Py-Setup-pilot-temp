import ssl
import pytest
from tornado.netutil import ssl_options_to_context

def test_ssl_options_to_context_returns_same_context():
    """Passing an existing SSLContext should return the same object."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    result = ssl_options_to_context(ctx)
    assert result is ctx, "Returned context should be the same instance"

def test_ssl_options_to_context_invalid_certfile_raises(tmp_path):
    """Providing a non‑existent certfile should raise FileNotFoundError."""
    non_existent = tmp_path / "no_such_cert.pem"
    options = {"certfile": str(non_existent)}
    with pytest.raises(FileNotFoundError):
        ssl_options_to_context(options)

def test_ssl_options_to_context_cert_none_disables_hostname():
    """When cert_reqs is CERT_NONE, check_hostname must be disabled."""
    options = {"cert_reqs": ssl.CERT_NONE}
    ctx = ssl_options_to_context(options)
    assert ctx.verify_mode == ssl.CERT_NONE, "verify_mode should be CERT_NONE"
    assert ctx.check_hostname is False, "check_hostname should be disabled for CERT_NONE"
