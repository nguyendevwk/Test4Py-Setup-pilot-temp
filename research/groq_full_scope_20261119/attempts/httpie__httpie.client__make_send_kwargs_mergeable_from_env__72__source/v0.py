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

def test_make_send_kwargs_verify_cases():
    for input_val, expected in (("YES", True), ("no", False), ("True", True), ("false", False), ("custom", "custom")):
        ns = argparse.Namespace(
            cert=None,
            cert_key=None,
            cert_key_pass=None,
            proxy=[],
            verify=input_val,
        )
        kwargs = make_send_kwargs_mergeable_from_env(ns)
        assert kwargs["verify"] == expected

def test_make_send_kwargs_cert_with_key_and_pass():
    ns = argparse.Namespace(
        cert="client.pem",
        cert_key="client.key",
        cert_key_pass=argparse.Namespace(value="passphrase"),
        proxy=[],
        verify="yes",
    )
    kwargs = make_send_kwargs_mergeable_from_env(ns)
    cert_obj = kwargs["cert"]
    assert isinstance(cert_obj, HTTPieCertificate)
    assert cert_obj.cert == "client.pem"
    assert cert_obj.key == "client.key"
    assert cert_obj.passphrase == "passphrase"
