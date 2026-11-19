import pytest
from dataclasses_json.cfg import Exclude

def test_always_returns_true_for_any_object():
    """`Exclude.ALWAYS` should return True for any input."""
    for value in (None, 0, 1, "", "test", [], [1, 2], {}, {"a": 1}):
        assert Exclude.ALWAYS(value) is True, f"ALWAYS failed for {value!r}"

def test_never_returns_false_for_any_object():
    """`Exclude.NEVER` should return False for any input."""
    for value in (None, 0, 1, "", "test", [], [1, 2], {}, {"a": 1}):
        assert Exclude.NEVER(value) is False, f"NEVER failed for {value!r}"

def test_exclude_callable_properties():
    """Both constants should be callable and have the expected signatures."""
    assert callable(Exclude.ALWAYS), "ALWAYS is not callable"
    assert callable(Exclude.NEVER), "NEVER is not callable"
    # Ensure they accept one positional argument
    try:
        Exclude.ALWAYS(42)
        Exclude.NEVER(42)
    except TypeError as exc:
        pytest.fail(f"Exclude constants do not accept a single argument: {exc}")
