import argparse
import pytest
from httpie.client import make_send_kwargs

def test_make_send_kwargs_with_timeout():
    """When a timeout is provided, it should be preserved in the kwargs."""
    args = argparse.Namespace(timeout=5.0, other="value")
    kwargs = make_send_kwargs(args)
    assert kwargs["timeout"] == 5.0
    assert kwargs["allow_redirects"] is False

def test_make_send_kwargs_without_timeout():
    """When timeout is None or falsy, the kwargs should contain None for timeout."""
    args = argparse.Namespace(timeout=None, other="value")
    kwargs = make_send_kwargs(args)
    assert kwargs["timeout"] is None
    assert kwargs["allow_redirects"] is False

def test_make_send_kwargs_missing_timeout_attribute():
    """If the args object lacks a timeout attribute, an AttributeError should be raised."""
    class DummyArgs:
        pass
    dummy = DummyArgs()
    with pytest.raises(AttributeError):
        make_send_kwargs(dummy)
