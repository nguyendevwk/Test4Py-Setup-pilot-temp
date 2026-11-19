import pytest
from sanic.helpers import Default


def test_default_repr_and_str():
    """Default should return the same string for repr and str."""
    d = Default()
    assert repr(d) == "<Default>"
    assert str(d) == "<Default>"


def test_default_identity_and_equality(tmp_path):
    """Each Default instance is distinct; equality is identity."""
    d1 = Default()
    d2 = Default()
    # They are different objects
    assert d1 is not d2
    # Equality falls back to identity
    assert (d1 == d2) is False
    # Store in a file to ensure no side effects
    file_path = tmp_path / "default.txt"
    file_path.write_text(str(d1))
    assert file_path.read_text() == "<Default>"


def test_default_hash_and_set_membership():
    """Default instances can be hashed and used in sets."""
    d = Default()
    s = {d}
    assert d in s
    # Another instance is not considered the same element
    assert Default() not in s
