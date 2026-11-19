import pytest
from pytutils.props import lazyclassproperty, classproperty


class Base:
    counter = 0

    @lazyclassproperty
    def value(cls):
        cls.counter += 1
        return cls.counter


class Derived(Base):
    pass


def test_lazyclassproperty_caches_value(tmp_path):
    # The property should be computed only once per class
    assert Base.value == 1
    assert Base.value == 1  # cached, no increment
    assert Base.counter == 1
    # Accessing via Derived should compute separately
    assert Derived.value == 1
    assert Derived.value == 1
    assert Derived.counter == 1
    # Ensure Base and Derived counters are independent
    assert Base.counter == 1
    assert Derived.counter == 1


def test_lazyclassproperty_inheritance_and_override(tmp_path):
    class Sub(Base):
        @lazyclassproperty
        def value(cls):
            # Override to return a different value
            return 42

    # Base uses its own implementation
    assert Base.value == 1
    # Sub overrides and caches its own value
    assert Sub.value == 42
    assert Sub.value == 42
    # Ensure counters reflect the correct number of evaluations
    assert Base.counter == 1
    assert Sub.counter == 0  # Sub's counter not used


def test_lazyclassproperty_error_propagation(tmp_path):
    class ErrorClass:
        @lazyclassproperty
        def bad(cls):
            raise ValueError("bad property")

    with pytest.raises(ValueError, match="bad property"):
        _ = ErrorClass.bad
    # Subsequent access should raise again, not cache the exception
    with pytest.raises(ValueError, match="bad property"):
        _ = ErrorClass.bad
