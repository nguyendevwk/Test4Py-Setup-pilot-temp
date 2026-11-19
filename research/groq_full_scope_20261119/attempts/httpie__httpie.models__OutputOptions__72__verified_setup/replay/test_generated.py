import pytest
from httpie.models import OutputOptions, RequestsMessageKind

def test_output_options_any_true():
    """`any` should return True when any flag is set."""
    opts = OutputOptions(kind=RequestsMessageKind.RESPONSE, headers=True, body=False, meta=False)
    assert opts.any() is True

def test_output_options_any_false():
    """`any` should return False when all flags are False."""
    opts = OutputOptions(kind=RequestsMessageKind.REQUEST, headers=False, body=False, meta=False)
    assert opts.any() is False

def test_output_options_default_meta():
    """`meta` defaults to False when not provided."""
    opts = OutputOptions(kind=RequestsMessageKind.RESPONSE, headers=True, body=True)
    assert opts.meta is False
    assert opts.headers is True
    assert opts.body is True
