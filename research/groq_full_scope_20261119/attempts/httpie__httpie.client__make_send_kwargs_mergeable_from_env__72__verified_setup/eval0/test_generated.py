import argparse
import pytest
from httpie.client import make_send_kwargs_mergeable_from_env
from httpie.ssl_ import HTTPieCertificate

def test_make_send_kwargs_normal():
    ns = argparse.Namespace(
        cert=None,
        cert_key=None,
        cert_key_pass=None,
        proxy=[argparse.Namespace(key="http", value="http://proxy")],
        verify="yes",
    )
    kwargs = make_send_kwargs_mergeable_from_env(ns)
    assert kwargs["proxies"] == {"http": "http://proxy"}
    assert kwargs["stream"] is True
    assert kwargs["verify"] is True
    assert kwargs["cert"] is None

def test_make_send_kwargs_verify_case_insensitive_and_invalid():
    ns = argparse.Namespace(
        cert=None,
        cert_key=None,
        cert_key_pass=None,
        proxy=[],
        verify="TrUe",
    )
    kwargs = make_send_kwargs_mergeable_from_env(ns)
    assert kwargs["verify"] is True

    ns_invalid = argparse.Namespace(
        cert=None,
        cert_key=None,
        cert_key_pass=None,
        proxy=[],
        verify="unknown",
    )
    kwargs_invalid = make_send_kwargs_mergeable_from_env(ns_invalid)
    assert kwargs_invalid["verify"] == "unknown"

def test_make_send_kwargs_cert_with_key_and_passphrase():
    ns = argparse.Namespace(
        cert="/path/to/cert.pem",
        cert_key="/path/to/key.pem",
        cert_key_pass=argparse.Namespace(value="passphrase"),
        proxy=[],
        verify="no",
    )
    kwargs = make_send_kwargs_mergeable_from_env(ns)
    cert_obj = kwargs["cert"]
    assert isinstance(cert_obj, HTTPieCertificate)
    # The certificate object should expose the original cert path
    assert cert_obj.cert == "/path/to/cert.pem"
    # The key and passphrase should be stored correctly
    assert cert_obj.key == "/path/to/key.pem"
    assert cert_obj.passphrase == "passphrase"
