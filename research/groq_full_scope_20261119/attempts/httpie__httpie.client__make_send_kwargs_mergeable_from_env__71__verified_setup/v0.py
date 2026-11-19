import argparse
import pytest
from httpie.client import make_send_kwargs_mergeable_from_env
from httpie.ssl_ import HTTPieCertificate

def test_make_send_kwargs_basic():
    """Verify that basic arguments are converted correctly."""
    ns = argparse.Namespace(
        cert=None,
        cert_key=None,
        cert_key_pass=None,
        proxy=[argparse.Namespace(key="http", value="http://proxy.example")],
        verify="yes",
    )
    kwargs = make_send_kwargs_mergeable_from_env(ns)
    assert kwargs["proxies"] == {"http": "http://proxy.example"}
    assert kwargs["stream"] is True
    assert kwargs["verify"] is True
    assert kwargs["cert"] is None

def test_make_send_kwargs_with_cert_and_key_and_passphrase():
    """Verify that cert, key and passphrase are wrapped in HTTPieCertificate."""
    ns = argparse.Namespace(
        cert="/path/to/cert.pem",
        cert_key="/path/to/key.pem",
        cert_key_pass=argparse.Namespace(value="s3cr3t"),
        proxy=[],
        verify="no",
    )
    kwargs = make_send_kwargs_mergeable_from_env(ns)
    cert_obj = kwargs["cert"]
    assert isinstance(cert_obj, HTTPieCertificate)
    # The HTTPieCertificate stores the cert, key and passphrase in its tuple
    assert cert_obj.cert == "/path/to/cert.pem"
    assert cert_obj.key == "/path/to/key.pem"
    assert cert_obj.passphrase == "s3cr3t"
    assert kwargs["verify"] is False
    assert kwargs["proxies"] == {}

def test_make_send_kwargs_verify_invalid_value():
    """Verify that an unknown verify value is returned unchanged."""
    ns = argparse.Namespace(
        cert=None,
        cert_key=None,
        cert_key_pass=None,
        proxy=[],
        verify="maybe",
    )
    kwargs = make_send_kwargs_mergeable_from_env(ns)
    # The mapping returns the original string when not found
    assert kwargs["verify"] == "maybe"
    assert kwargs["cert"] is None
    assert kwargs["proxies"] == {}
