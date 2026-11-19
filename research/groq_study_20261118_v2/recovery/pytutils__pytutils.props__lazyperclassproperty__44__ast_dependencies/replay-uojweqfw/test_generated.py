import pytest
from pytutils.props import lazyperclassproperty


def test_lazyperclassproperty_caches_per_class():
    """The decorator should compute the value once per class and cache it."""
    calls = []

    @lazyperclassproperty
    def value(cls):
        calls.append(cls.__name__)
        return f"computed-{cls.__name__}"

    class Base:
        prop = value

    class Child(Base):
        pass

    # First access on Base triggers computation
    assert Base.prop == "computed-Base"
    assert calls == ["Base"]

    # Second access on Base should use cached value
    assert Base.prop == "computed-Base"
    assert calls == ["Base"]

    # Access on Child triggers a new computation
    assert Child.prop == "computed-Child"
    assert calls == ["Base", "Child"]

    # Subsequent access on Child uses cached value
    assert Child.prop == "computed-Child"
    assert calls == ["Base", "Child"]


def test_lazyperclassproperty_attribute_name_is_unique():
    """The cached attribute name should include the class name to avoid clashes."""
    @lazyperclassproperty
    def value(cls):
        return f"{cls.__name__}-value"

    class A:
        prop = value

    class B:
        prop = value

    # Ensure that accessing A.prop does not affect B.prop
    assert A.prop == "A-value"
    assert B.prop == "B-value"
    # The attribute names should be distinct
    assert hasattr(A, "_A_lazy_value")
    assert hasattr(B, "_B_lazy_value")
    assert not hasattr(A, "_B_lazy_value")
    assert not hasattr(B, "_A_lazy_value")


def test_lazyperclassproperty_exception_propagates():
    """If the wrapped function raises, the exception should propagate and not be cached."""
    @lazyperclassproperty
    def value(cls):
        raise RuntimeError("boom")

    class C:
        prop = value

    with pytest.raises(RuntimeError, match="boom"):
        _ = C.prop

    # Subsequent access should still raise and not cache a value
    with pytest.raises(RuntimeError, match="boom"):
        _ = C.prop


def test_lazyperclassproperty_with_inheritance_and_overriding():
    """Subclass can override the property with a different implementation."""
    @lazyperclassproperty
    def value(cls):
        return f"base-{cls.__name__}"

    class Parent:
        prop = value

    @lazyperclassproperty
    def value(cls):
        return f"child-{cls.__name__}"

    class Child(Parent):
        prop = value

    # Parent uses its own implementation
    assert Parent.prop == "base-Parent"
    # Child uses its overridden implementation
    assert Child.prop == "child-Child"


def test_lazyperclassproperty_is_readonly():
    """Attempting to set the property should raise AttributeError."""
    @lazyperclassproperty
    def value(cls):
        return 42

    class D:
        prop = value

    with pytest.raises(AttributeError):
        D.prop = 99
