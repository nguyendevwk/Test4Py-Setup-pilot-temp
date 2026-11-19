import argparse
import pytest
from httpie.client import make_send_kwargs_mergeable_from_env
from httpie.ssl_ import HTTPieCertificate

class DummyPass:
    def __init__(self, value):
        self.value = value

def test_make_send_kwargs_normal_behavior():
    ns = argparse.Namespace(
        cert="client.pem",
        cert_key="key.pem",
        cert_key_pass=DummyPass("passphrase"),
        proxy=[argparse.Namespace(key="http", value="http://proxy.example")],
        verify="yes",
    )
    kwargs = make_send_kwargs_mergeable_from_env(ns)
    assert kwargs["stream"] is True
    assert kwargs["proxies"] == {"http": "http://proxy.example"}
    assert kwargs["verify"] is True
    assert isinstance(kwargs["cert"], HTTPieCertificate)
    assert kwargs["cert"].cert == "client.pem"
    assert kwargs["cert"].key == "key.pem"
    assert kwargs["cert"].passphrase == "passphrase"

def test_make_send_kwargs_verify_mapping_unknown():
    ns = argparse.Namespace(
        cert=None,
        cert_key=None,
        cert_key_pass=None,
        proxy=[],
        verify="maybe",
    )
    kwargs = make_send_kwargs_mergeable_from_env(ns)
    assert kwargs["verify"] == "maybe"

def test_make_send_kwargs_no_cert_and_no_proxy():
    ns = argparse.Namespace(
        cert=None,
        cert_key=None,
        cert_key_pass=None,
        proxy=[],
        verify="no",
    )
    kwargs = make_send_kwargs_mergeable_from_env(ns)
    assert kwargs["cert"] is None
    assert kwargs["proxies"] == {}
    assert kwargs["verify"] is False
