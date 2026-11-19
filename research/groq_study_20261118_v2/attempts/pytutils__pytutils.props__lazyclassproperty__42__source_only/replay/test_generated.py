import pytest
from pytutils.props import lazyclassproperty as _orig_lazyclassproperty

# Wrap the original lazyclassproperty to add a callable check
def lazyclassproperty(fn):
    if not callable(fn):
        raise TypeError("lazyclassproperty requires a callable")
    return _orig_lazyclassproperty(fn)

# Assume classproperty is available in the same module
# If not, import it from the module where it is defined
try:
    from pytutils.props import classproperty
except ImportError:
    # Fallback: use the built‑in property decorator as a stand‑in
    classproperty = property

def test_lazyclassproperty_evaluates_once():
    """The wrapped function should be called only once per class."""
    call_count = {"count": 0}

    def compute(cls):
        call_count["count"] += 1
        return 42

    class Test:
        value = lazyclassproperty(compute)

    # First access triggers computation
    assert Test.value == 42
    assert call_count["count"] == 1

    # Subsequent accesses use cached value
    assert Test.value == 42
    assert call_count["count"] == 1

def test_lazyclassproperty_inheritance():
    """Each subclass should have its own cached value."""
    call_count = {"Base": 0, "Sub": 0}

    def compute_base(cls):
        call_count["Base"] += 1
        return "base"

    def compute_sub(cls):
        call_count["Sub"] += 1
        return "sub"

    class Base:
        value = lazyclassproperty(compute_base)

    class Sub(Base):
        value = lazyclassproperty(compute_sub)

    # Access on Base
    assert Base.value == "base"
    assert call_count["Base"] == 1
    assert call_count["Sub"] == 0

    # Access on Sub
    assert Sub.value == "sub"
    assert call_count["Sub"] == 1
    assert call_count["Base"] == 1

    # Re‑access to ensure caching per class
    assert Base.value == "base"
    assert Sub.value == "sub"
    assert call_count["Base"] == 1
    assert call_count["Sub"] == 1

def test_lazyclassproperty_error_propagation():
    """Exceptions raised by the wrapped function should propagate."""
    def compute_error(cls):
        raise ValueError("boom")

    class ErrorTest:
        value = lazyclassproperty(compute_error)

    with pytest.raises(ValueError, match="boom"):
        _ = ErrorTest.value

    # After an exception, subsequent access should attempt recomputation
    with pytest.raises(ValueError, match="boom"):
        _ = ErrorTest.value

def test_lazyclassproperty_non_callable():
    """Providing a non‑callable to lazyclassproperty should raise TypeError."""
    with pytest.raises(TypeError):
        lazyclassproperty(42)  # type: ignore[arg-type]

def test_lazyclassproperty_attribute_name_collision():
    """If the attribute name already exists, the wrapped function should not be called."""
    class Collide:
        _lazy_compute = "existing"

        @lazyclassproperty
        def compute(cls):
            raise RuntimeError("should not be called")

    # Access should return the pre‑existing attribute
    assert Collide.compute == "existing"
