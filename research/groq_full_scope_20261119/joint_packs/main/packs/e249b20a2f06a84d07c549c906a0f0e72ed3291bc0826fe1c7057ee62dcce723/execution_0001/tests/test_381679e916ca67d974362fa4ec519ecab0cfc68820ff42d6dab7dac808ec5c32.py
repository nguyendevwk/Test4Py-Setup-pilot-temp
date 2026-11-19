import pytest
from apimd.parser import is_public_family

def test_public_names_are_true(tmp_path):
    # A simple public name should return True
    assert is_public_family("module") is True
    # A dotted public name should also return True
    assert is_public_family("package.module") is True
    # Names containing magic identifiers are ignored for privacy checks
    assert is_public_family("__init__") is True
    assert is_public_family("pkg.__main__") is True
    # Mixed magic and public parts still return True
    assert is_public_family("pkg.__init__.module") is True

def test_private_names_are_false(tmp_path):
    # Leading underscore marks a private name
    assert is_public_family("_private") is False
    # Private part in a dotted name makes the whole name private
    assert is_public_family("pkg._private.module") is False
    # Multiple private parts still result in False
    assert is_public_family("_pkg._private") is False

def test_edge_cases_and_empty_string(tmp_path):
    # Empty string should be considered public (no private parts)
    assert is_public_family("") is True
    # Name with only magic parts is public
    assert is_public_family("__all__") is True
    # Name with trailing dot should be treated as public (no private part)
    assert is_public_family("module.") is True
    # Name with internal dots but no private parts
    assert is_public_family("a.b.c") is True
