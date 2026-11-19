import argparse
import pytest
from httpie.client import make_send_kwargs

def test_make_send_kwargs_with_timeout():
    """Normal case: timeout is set to a positive value."""
    ns = argparse.Namespace(timeout=5, other="value")
    kwargs = make_send_kwargs(ns)
    assert kwargs == {"timeout": 5, "allow_redirects": False}

def test_make_send_kwargs_without_timeout():
    """Boundary case: timeout is None, should be passed as None."""
    ns = argparse.Namespace(timeout=None, other="value")
    kwargs = make_send_kwargs(ns)
    assert kwargs == {"timeout": None, "allow_redirects": False}

def test_make_send_kwargs_missing_timeout_attribute():
    """Error case: Namespace lacks 'timeout' attribute, should raise AttributeError."""
    class Dummy:
        pass
    dummy = Dummy()
    with pytest.raises(AttributeError):
        make_send_kwargs(dummy)
