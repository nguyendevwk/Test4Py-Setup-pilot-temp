import pytest
from dataclasses_json.cfg import Exclude

def test_exclude_always_returns_true_for_any_object():
    """Exclude.ALWAYS should return True for any input."""
    for obj in (None, 0, 1, "", "test", [], {}, set(), object()):
        assert Exclude.ALWAYS(obj) is True, f"ALWAYS returned {Exclude.ALWAYS(obj)} for {obj!r}"

def test_exclude_never_returns_false_for_any_object():
    """Exclude.NEVER should return False for any input."""
    for obj in (None, 0, 1, "", "test", [], {}, set(), object()):
        assert Exclude.NEVER(obj) is False, f"NEVER returned {Exclude.NEVER(obj)} for {obj!r}"

def test_exclude_functions_are_distinct_and_callable():
    """Ensure that ALWAYS and NEVER are distinct callables and can be called."""
    assert Exclude.ALWAYS is not Exclude.NEVER, "ALWAYS and NEVER should be different functions"
    # Call each once to confirm no exception is raised
    try:
        Exclude.ALWAYS(42)
        Exclude.NEVER(42)
    except Exception as exc:
        pytest.fail(f"Calling Exclude functions raised an exception: {exc}")
