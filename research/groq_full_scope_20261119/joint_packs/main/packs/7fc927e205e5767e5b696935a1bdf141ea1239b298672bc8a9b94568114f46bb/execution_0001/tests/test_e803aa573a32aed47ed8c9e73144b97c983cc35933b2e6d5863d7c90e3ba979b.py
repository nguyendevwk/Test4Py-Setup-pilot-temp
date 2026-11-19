import pytest
from apimd.parser import is_public_family

def test_public_name_returns_true():
    # A fully qualified public name should return True
    assert is_public_family("module.submodule.Class") is True

def test_private_name_returns_false():
    # Any component starting with '_' should cause False
    assert is_public_family("module._private.Class") is False
    assert is_public_family("_module.submodule.Class") is False

def test_magic_name_is_ignored_and_public():
    # Magic names like __init__ should be ignored and not affect the result
    assert is_public_family("module.__init__.Class") is True
    assert is_public_family("__main__.module.Class") is True
