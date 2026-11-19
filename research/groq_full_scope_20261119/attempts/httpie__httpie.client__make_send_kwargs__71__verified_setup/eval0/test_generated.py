import argparse
import pytest
from httpie.client import make_send_kwargs

def test_make_send_kwargs_with_timeout():
    """Normal case: timeout is set to a positive value."""
    ns = argparse.Namespace(timeout=5, other="value")
    kwargs = make_send_kwargs(ns)
    assert kwargs == {"timeout": 5, "allow_redirects": False}

def test_make_send_kwargs_boundary_zero_timeout():
    """Boundary case: timeout is zero, which should be preserved."""
    ns = argparse.Namespace(timeout=0, other="value")
    kwargs = make_send_kwargs(ns)
    assert kwargs == {"timeout": 0, "allow_redirects": False}

def test_make_send_kwargs_missing_timeout_attribute():
    """Error case: Namespace lacks a 'timeout' attribute, should raise AttributeError."""
    class Dummy:
        pass
    dummy = Dummy()
    with pytest.raises(AttributeError):
        make_send_kwargs(dummy)
