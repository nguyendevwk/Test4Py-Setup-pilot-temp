import pytest
from pytutils.props import lazyclassproperty

# Helper class to expose the underlying classproperty for introspection
class Dummy:
    @lazyclassproperty
    def value(cls):
        return 42

class SubDummy(Dummy):
    pass

def test_lazyclassproperty_caches_value(tmp_path):
    # The value should be computed only once and cached on the class
    assert Dummy.value == 42
    # Modify the underlying function to see if cache prevents recomputation
    original_fn = Dummy.value.fget
    Dummy.value.fget = lambda cls: 99  # replace the function
    # The cached value should still be 42
    assert Dummy.value == 42
    # Restore original function for other tests
    Dummy.value.fget = original_fn

def test_lazyclassproperty_inheritance_and_cache(tmp_path):
    # Subclass should inherit the property and compute its own cache
    assert SubDummy.value == 42
    # Ensure that the subclass has its own cached attribute, not the base's
    assert hasattr(SubDummy, "_lazy_value")
    assert not hasattr(Dummy, "_lazy_value") or Dummy._lazy_value == 42
    # Changing the base's cached value should not affect the subclass
    Dummy._lazy_value = 100
    assert SubDummy.value == 42

def test_lazyclassproperty_error_propagation(tmp_path):
    # Define a property that raises an exception
    class ErrorDummy:
        @lazyclassproperty
        def bad(cls):
            raise ValueError("bad property")

    with pytest.raises(ValueError, match="bad property"):
        _ = ErrorDummy.bad
    # After the exception, the attribute should not be set
    assert not hasattr(ErrorDummy, "_lazy_bad")
