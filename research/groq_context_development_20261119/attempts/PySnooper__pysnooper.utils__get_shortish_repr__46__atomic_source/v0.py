import pytest
from pysnooper.utils import get_shortish_repr

class Dummy:
    def __repr__(self):
        return "DummyRepresentation"

def test_normal_repr_and_truncate():
    # Normal representation without custom or normalization
    result = get_shortish_repr(Dummy())
    assert result == "DummyRepresentation"

    # Truncate to a shorter length
    truncated = get_shortish_repr(Dummy(), max_length=5)
    assert truncated == "Dummy"

def test_custom_repr_and_normalize():
    # Custom repr function that returns a multi-line string
    def custom_repr(obj):
        return f"Custom\n{obj.__class__.__name__}\nRepresentation"

    result = get_shortish_repr(Dummy(), custom_repr=(custom_repr,))
    # Newlines should be removed
    assert result == "CustomDummyRepresentation"

    # With normalization, whitespace should be collapsed
    normalized = get_shortish_repr(Dummy(), custom_repr=(custom_repr,), normalize=True)
    assert normalized == "Custom Dummy Representation"

def test_repr_failure_and_error_handling():
    # Object whose __repr__ raises an exception
    class BadRepr:
        def __repr__(self):
            raise ValueError("bad repr")

    result = get_shortish_repr(BadRepr())
    assert result == "REPR FAILED"

    # Ensure that even with max_length, the failure string is returned unchanged
    truncated = get_shortish_repr(BadRepr(), max_length=10)
    assert truncated == "REPR FAILED"
