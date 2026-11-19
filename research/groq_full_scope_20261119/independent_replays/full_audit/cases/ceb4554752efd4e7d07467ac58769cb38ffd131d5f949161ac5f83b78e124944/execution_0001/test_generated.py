import pytest
from flutils.objutils import has_callables

def test_has_callables_with_builtin_dict_methods():
    # Normal case: all attributes exist and are callable
    assert has_callables(dict(), "get", "keys", "items", "values") is True

def test_has_callables_with_non_callable_attribute():
    # Boundary case: attribute exists but is not callable
    class Dummy:
        x = 42
    assert has_callables(Dummy(), "x") is False

def test_has_callables_with_missing_attribute():
    # Error case: attribute does not exist
    class Dummy:
        pass
    assert has_callables(Dummy(), "missing") is False
