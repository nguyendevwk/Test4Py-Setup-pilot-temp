import pytest
from types import FunctionType

# Import the target function from the production module
from pytutils.props import lazyperclassproperty

# Helper class to provide a classproperty decorator if not already defined
# (the production code assumes a classproperty decorator exists; we provide a minimal one for testing)
def classproperty(func):
    class ClassPropertyDescriptor:
        def __get__(self, obj, owner):
            return func(owner)
    return ClassPropertyDescriptor()


# Patch the module to include the classproperty decorator for the test environment
import pytutils.props
pytutils.props.classproperty = classproperty


def test_lazyperclassproperty_computes_once_per_class():
    """The wrapped function should be called only once per class and cached."""
    call_count = {"count": 0}

    def compute(cls):
        call_count["count"] += 1
        return f"value_for_{cls.__name__}"

    @lazyperclassproperty
    def prop(cls):
        return compute(cls)

    class Base:
        lazy_prop = prop

    class Derived(Base):
        pass

    # First access on Base triggers computation
    assert Base.lazy_prop == "value_for_Base"
    assert call_count["count"] == 1

    # Second access on Base uses cached value
    assert Base.lazy_prop == "value_for_Base"
    assert call_count["count"] == 1

    # Access on Derived triggers a separate computation
    assert Derived.lazy_prop == "value_for_Derived"
    assert call_count["count"] == 2

    # Subsequent access on Derived uses cached value
    assert Derived.lazy_prop == "value_for_Derived"
    assert call_count["count"] == 2


def test_lazyperclassproperty_inheritance_and_override():
    """Subclasses should not share cached values unless they override the property."""
    call_log = []

    def compute(cls):
        call_log.append(cls.__name__)
        return f"cached_{cls.__name__}"

    @lazyperclassproperty
    def prop(cls):
        return compute(cls)

    class Parent:
        lazy_prop = prop

    class Child(Parent):
        pass

    # Access on Parent and Child
    assert Parent.lazy_prop == "cached_Parent"
    assert Child.lazy_prop == "cached_Child"
    assert call_log == ["Parent", "Child"]

    # Override property in Child
    @lazyperclassproperty
    def prop(cls):
        return f"overridden_{cls.__name__}"

    Child.lazy_prop = prop

    # Access after override
    assert Child.lazy_prop == "overridden_Child"
    # Parent remains unchanged
    assert Parent.lazy_prop == "cached_Parent"
    # No new call for Parent
    assert call_log == ["Parent", "Child"]


def test_lazyperclassproperty_error_propagation():
    """If the wrapped function raises, the exception should propagate and not be cached."""
    def compute(cls):
        raise ValueError(f"Error in {cls.__name__}")

    @lazyperclassproperty
    def prop(cls):
        return compute(cls)

    class TestCls:
        lazy_prop = prop

    with pytest.raises(ValueError, match="Error in TestCls"):
        _ = TestCls.lazy_prop

    # Subsequent access should raise again, not return a cached value
    with pytest.raises(ValueError, match="Error in TestCls"):
        _ = TestCls.lazy_prop


def test_lazyperclassproperty_attribute_name_is_unique():
    """The attribute name used for caching should be unique per class and property."""
    def compute(cls):
        return f"unique_{cls.__name__}"

    @lazyperclassproperty
    def prop(cls):
        return compute(cls)

    class A:
        lazy_prop = prop

    class B:
        lazy_prop = prop

    # Access to trigger caching
    assert A.lazy_prop == "unique_A"
    assert B.lazy_prop == "unique_B"

    # Verify that the internal attribute names differ
    attr_a = f"_A_lazy_prop"
    attr_b = f"_B_lazy_prop"
    assert hasattr(A, attr_a)
    assert hasattr(B, attr_b)
    assert not hasattr(A, attr_b)
    assert not hasattr(B, attr_a)
