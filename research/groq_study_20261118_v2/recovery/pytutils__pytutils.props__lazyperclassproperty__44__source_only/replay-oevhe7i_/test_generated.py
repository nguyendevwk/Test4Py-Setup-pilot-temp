import pytest
from pytutils.props import lazyperclassproperty

# Helper class to track calls
class CallCounter:
    def __init__(self):
        self.calls = 0

    def __call__(self, cls):
        self.calls += 1
        return f"computed_for_{cls.__name__}"


def test_lazyperclassproperty_computes_once_per_class():
    counter = CallCounter()

    class Base:
        @lazyperclassproperty
        def value(cls):
            return counter(cls)

    # First access triggers computation
    assert Base.value == "computed_for_Base"
    assert counter.calls == 1

    # Subsequent access uses cached value
    assert Base.value == "computed_for_Base"
    assert counter.calls == 1  # still one call


def test_lazyperclassproperty_is_isolated_per_subclass():
    counter = CallCounter()

    class Base:
        @lazyperclassproperty
        def value(cls):
            return counter(cls)

    class Sub(Base):
        pass

    # Access on Base
    assert Base.value == "computed_for_Base"
    # Access on Sub
    assert Sub.value == "computed_for_Sub"

    # Each class computed once
    assert counter.calls == 2
    # Cached values are distinct
    assert Base.value != Sub.value


def test_lazyperclassproperty_attribute_name_is_unique():
    counter = CallCounter()

    class Base:
        @lazyperclassproperty
        def foo(cls):
            return counter(cls)

    # Access to create attribute
    _ = Base.foo
    # Attribute name should be constructed correctly
    expected_attr = f"_Base_lazy_foo"
    assert hasattr(Base, expected_attr)
    assert getattr(Base, expected_attr) == "computed_for_Base"


def test_lazyperclassproperty_raises_on_error():
    def faulty(cls):
        raise ValueError("bad")

    class Bad:
        @lazyperclassproperty
        def prop(cls):
            return faulty(cls)

    with pytest.raises(ValueError, match="bad"):
        _ = Bad.prop

    # Subsequent access should raise again, not cache the exception
    with pytest.raises(ValueError, match="bad"):
        _ = Bad.prop
