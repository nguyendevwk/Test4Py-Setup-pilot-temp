import pytest
from pytutils.props import lazyperclassproperty

# Helper to count calls
def make_counter():
    count = {"n": 0}
    def counter(cls):
        count["n"] += 1
        return f"value-{cls.__name__}"
    return counter, count

class Base:
    pass

class Derived(Base):
    pass

def test_lazyperclassproperty_caches_value_per_class():
    counter, count = make_counter()
    class Test(Base):
        @lazyperclassproperty
        def prop(cls):
            return counter(cls)

    # First access triggers computation
    assert Test.prop == "value-Test"
    assert count["n"] == 1

    # Subsequent access uses cached value
    assert Test.prop == "value-Test"
    assert count["n"] == 1

def test_lazyperclassproperty_separate_cache_for_subclass():
    counter, count = make_counter()
    class Test(Base):
        @lazyperclassproperty
        def prop(cls):
            return counter(cls)

    class Sub(Test):
        pass

    # Access on base class
    assert Test.prop == "value-Test"
    assert count["n"] == 1

    # Access on subclass triggers separate computation
    assert Sub.prop == "value-Sub"
    assert count["n"] == 2

    # Re-access on subclass uses cached value
    assert Sub.prop == "value-Sub"
    assert count["n"] == 2

def test_lazyperclassproperty_raises_exception_on_failure():
    def failing(cls):
        raise RuntimeError("fail")

    class Test(Base):
        @lazyperclassproperty
        def prop(cls):
            return failing(cls)

    with pytest.raises(RuntimeError, match="fail"):
        _ = Test.prop

    # Subsequent access still raises, but does not cache the exception
    with pytest.raises(RuntimeError, match="fail"):
        _ = Test.prop
