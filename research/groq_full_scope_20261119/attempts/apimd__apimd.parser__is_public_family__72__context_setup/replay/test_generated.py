import pytest
from apimd.parser import is_public_family

def test_public_names_without_private_parts():
    # Names that are fully public should return True
    assert is_public_family("module.submodule.Class") is True
    assert is_public_family("pkg.__init__") is True  # magic name allowed
    assert is_public_family("pkg.__main__") is True  # magic name allowed

def test_private_names_with_leading_underscore():
    # Any part starting with '_' should cause False
    assert is_public_family("_private") is False
    assert is_public_family("module._private.Class") is False
    assert is_public_family("module.submodule._Class") is False
    # Magic names are ignored, so a leading underscore before a magic name still fails
    assert is_public_family("_private.__init__") is False

def test_mixed_magic_and_private_parts():
    # Mixed names where magic parts are present but private parts exist
    assert is_public_family("pkg.__init__._private") is False
    assert is_public_family("pkg._private.__main__") is False
    # Pure magic parts are allowed even if other parts are magic
    assert is_public_family("__main__") is True
    assert is_public_family("pkg.__main__") is True
