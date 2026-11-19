import pytest
from pytutils.props import lazyperclassproperty

# Assume classproperty is available in the same module
from pytutils.props import classproperty


def test_lazyperclassproperty_caches_per_class(tmp_path):
    """The property should compute once per class and cache the result."""
    counter = {"count": 0}

    class Base:
        @lazyperclassproperty
        def value(cls):
            counter["count"] += 1
            return f"Base-{cls.__name__}"

    # First access triggers computation
    assert Base.value == "Base-Base"
    assert counter["count"] == 1

    # Second access uses cached value
    assert Base.value == "Base-Base"
    assert counter["count"] == 1

    # Subclass gets its own cached value
    class Sub(Base):
        pass

    assert Sub.value == "Base-Sub"
    assert counter["count"] == 2

    # Subsequent access on subclass uses its cache
    assert Sub.value == "Base-Sub"
    assert counter["count"] == 2


def test_lazyperclassproperty_is_independent_of_instance(tmp_path):
    """Accessing the property via an instance should return the same cached value."""
    class MyClass:
        @lazyperclassproperty
        def data(cls):
            return f"data-{cls.__name__}"

    instance = MyClass()
    assert instance.data == MyClass.data
    assert instance.data == "data-MyClass"


def test_lazyperclassproperty_raises_on_error(tmp_path):
    """If the underlying function raises, the exception propagates and is not cached."""
    class Faulty:
        @lazyperclassproperty
        def broken(cls):
            raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        _ = Faulty.broken

    # Subsequent access should still raise, not cache the exception
    with pytest.raises(ValueError, match="boom"):
        _ = Faulty.broken
