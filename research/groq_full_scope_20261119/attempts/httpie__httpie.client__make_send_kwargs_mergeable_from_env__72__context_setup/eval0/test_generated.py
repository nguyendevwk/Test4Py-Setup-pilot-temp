import argparse
import pytest
from httpie.client import make_send_kwargs_mergeable_from_env
from httpie.ssl_ import HTTPieCertificate

def test_make_send_kwargs_normal_and_verify_mapping():
    # Normal arguments: no cert, simple proxies, verify mapping
    args = argparse.Namespace(
        cert=None,
        cert_key=None,
        cert_key_pass=None,
        proxy=[argparse.Namespace(key="http", value="http://proxy.example")],
        verify="yes",
    )
    kwargs = make_send_kwargs_mergeable_from_env(args)
    assert kwargs["proxies"] == {"http": "http://proxy.example"}
    assert kwargs["stream"] is True
    # verify mapping should resolve to True
    assert kwargs["verify"] is True
    # cert should be None
    assert kwargs["cert"] is None

def test_make_send_kwargs_verify_case_insensitivity_and_false():
    # Verify values should be case-insensitive and map to bool
    for input_value, expected in (("TRUE", True), ("False", False), ("no", False), ("YES", True)):
        args = argparse.Namespace(
            cert=None,
            cert_key=None,
            cert_key_pass=None,
            proxy=[],
            verify=input_value,
        )
        kwargs = make_send_kwargs_mergeable_from_env(args)
        assert kwargs["verify"] is expected

def test_make_send_kwargs_with_client_cert_and_key():
    # When cert and cert_key are provided, cert should be an HTTPieCertificate instance
    args = argparse.Namespace(
        cert="/path/to/cert.pem",
        cert_key="/path/to/key.pem",
        cert_key_pass=argparse.Namespace(value="passphrase"),
        proxy=[],
        verify="no",
    )
    kwargs = make_send_kwargs_mergeable_from_env(args)
    cert_obj = kwargs["cert"]
    assert isinstance(cert_obj, HTTPieCertificate)
    # The certificate tuple should contain the cert path, key path, and passphrase
    assert cert_obj.cert == "/path/to/cert.pem"
    assert cert_obj.key == "/path/to/key.pem"
    assert cert_obj.passphrase == "passphrase"
    # verify should be False
    assert kwargs["verify"] is False
