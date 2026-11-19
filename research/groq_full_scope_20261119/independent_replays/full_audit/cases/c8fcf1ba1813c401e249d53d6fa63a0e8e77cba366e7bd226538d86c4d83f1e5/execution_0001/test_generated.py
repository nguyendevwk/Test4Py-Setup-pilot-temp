import argparse
import pytest
from httpie.client import make_send_kwargs

def test_make_send_kwargs_with_timeout():
    """When a positive timeout is provided, it should be preserved."""
    ns = argparse.Namespace(timeout=5.0)
    kwargs = make_send_kwargs(ns)
    assert kwargs["timeout"] == 5.0
    assert kwargs["allow_redirects"] is False

def test_make_send_kwargs_without_timeout():
    """When timeout is None, the keyword should be None."""
    ns = argparse.Namespace(timeout=None)
    kwargs = make_send_kwargs(ns)
    assert kwargs["timeout"] is None
    assert kwargs["allow_redirects"] is False

def test_make_send_kwargs_with_zero_timeout():
    """Zero timeout should be treated as falsy and result in None."""
    ns = argparse.Namespace(timeout=0)
    kwargs = make_send_kwargs(ns)
    assert kwargs["timeout"] is None
    assert kwargs["allow_redirects"] is False
