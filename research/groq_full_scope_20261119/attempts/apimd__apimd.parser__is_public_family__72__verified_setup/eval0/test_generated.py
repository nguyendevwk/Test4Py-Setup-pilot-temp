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
    # Magic names like __init__ are ignored; the rest must be public
    assert is_public_family("__init__.module.Class") is True
    # If all components are magic, still True
    assert is_public_family("__init__.__main__") is True
