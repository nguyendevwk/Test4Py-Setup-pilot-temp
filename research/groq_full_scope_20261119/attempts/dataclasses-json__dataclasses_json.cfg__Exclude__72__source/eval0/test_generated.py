import pytest
from dataclasses_json.cfg import Exclude

def test_always_exclusion_returns_true():
    """Exclude.ALWAYS should return True for any input."""
    assert Exclude.ALWAYS(1) is True
    assert Exclude.ALWAYS("foo") is True
    assert Exclude.ALWAYS(None) is True
    assert Exclude.ALWAYS([]) is True

def test_never_exclusion_returns_false():
    """Exclude.NEVER should return False for any input."""
    assert Exclude.NEVER(1) is False
    assert Exclude.NEVER("foo") is False
    assert Exclude.NEVER(None) is False
    assert Exclude.NEVER([]) is False

def test_exclusion_callable_is_callable_and_has_expected_signature():
    """Both Exclude constants must be callable and accept a single argument."""
    for func in (Exclude.ALWAYS, Exclude.NEVER):
        assert callable(func)
        # Ensure calling with a single argument does not raise TypeError
        try:
            result = func(42)
        except TypeError as exc:
            pytest.fail(f"Callable raised TypeError: {exc}")
        # The result should be a boolean
        assert isinstance(result, bool)
