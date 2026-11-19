import pytest
from pytutils.props import lazyperclassproperty


def test_lazyperclassproperty_caches_per_class(tmp_path):
    """The property should compute once per class and cache the result."""
    counter = {"count": 0}

    @lazyperclassproperty
    def value(cls):
        counter["count"] += 1
        return f"{cls.__name__}_value"

    class Base:
        pass

    class Child(Base):
        pass

    # First access on Base triggers computation
    assert Base.value == "Base_value"
    assert counter["count"] == 1

    # Second access on Base uses cache
    assert Base.value == "Base_value"
    assert counter["count"] == 1

    # Access on Child triggers its own computation
    assert Child.value == "Child_value"
    assert counter["count"] == 2

    # Child's cache is independent
    assert Child.value == "Child_value"
    assert counter["count"] == 2

    # Base's cache remains unchanged
    assert Base.value == "Base_value"
    assert counter["count"] == 2


def test_lazyperclassproperty_access_via_instance(tmp_path):
    """Accessing the property through an instance should return the same cached value."""
    counter = {"count": 0}

    @lazyperclassproperty
    def value(cls):
        counter["count"] += 1
        return f"{cls.__name__}_value"

    class MyClass:
        pass

    instance = MyClass()
    # First access via class triggers computation
    assert MyClass.value == "MyClass_value"
    assert counter["count"] == 1

    # Access via instance uses the same cached value
    assert instance.value == "MyClass_value"
    assert counter["count"] == 1


def test_lazyperclassproperty_inheritance_and_overriding(tmp_path):
    """Subclass can override the property and maintain its own cache."""
    counter = {"Base": 0, "Sub": 0}

    @lazyperclassproperty
    def value(cls):
        counter[cls.__name__] += 1
        return f"{cls.__name__}_value"

    class Base:
        pass

    class Sub(Base):
        pass

    # Base and Sub each compute once
    assert Base.value == "Base_value"
    assert Sub.value == "Sub_value"
    assert counter["Base"] == 1
    assert counter["Sub"] == 1

    # Overriding the property in Sub
    @lazyperclassproperty
    def value(cls):
        counter[cls.__name__] += 1
        return f"{cls.__name__}_overridden"

    class SubOverride(Sub):
        pass

    # SubOverride uses its own overridden implementation
    assert SubOverride.value == "SubOverride_overridden"
    assert counter["SubOverride"] == 1

    # Base remains unchanged
    assert Base.value == "Base_value"
    assert counter["Base"] == 1


def test_lazyperclassproperty_error_propagation():
    """If the underlying function raises, the exception propagates and is not cached."""
    @lazyperclassproperty
    def value(cls):
        raise ValueError("boom")

    class ErrorClass:
        pass

    with pytest.raises(ValueError, match="boom"):
        _ = ErrorClass.value

    # Subsequent access still raises and does not cache the exception
    with pytest.raises(ValueError, match="boom"):
        _ = ErrorClass.value
