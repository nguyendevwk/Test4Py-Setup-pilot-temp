import pytest
from pytutils.props import lazyperclassproperty


class Base:
    call_count = 0

    @lazyperclassproperty
    def value(cls):
        Base.call_count += 1
        return f"Base-{cls.__name__}"


class SubA(Base):
    pass


class SubB(Base):
    pass


def test_lazyperclassproperty_computes_once_per_class():
    # First access triggers computation
    assert Base.value == "Base-Base"
    assert Base.call_count == 1

    # Subsequent access uses cached value
    assert Base.value == "Base-Base"
    assert Base.call_count == 1

    # Subclass accesses compute separately
    assert SubA.value == "Base-SubA"
    assert Base.call_count == 2  # SubA triggers new computation

    # SubB also computes separately
    assert SubB.value == "Base-SubB"
    assert Base.call_count == 3

    # Re-accessing subclasses uses cached values
    assert SubA.value == "Base-SubA"
    assert SubB.value == "Base-SubB"
    assert Base.call_count == 3


def test_lazyperclassproperty_is_class_property():
    # The property should be accessible via the class, not via an instance
    instance = Base()
    # Accessing via instance should return the same cached value
    assert instance.value == Base.value
    # Ensure that the attribute is not stored on the instance
    assert not hasattr(instance, "_Base_lazy_value")


def test_lazyperclassproperty_error_propagation():
    # Define a property that raises an exception on first call
    class ErrorClass:
        @lazyperclassproperty
        def problematic(cls):
            raise RuntimeError("Intentional failure")

    with pytest.raises(RuntimeError, match="Intentional failure"):
        _ = ErrorClass.problematic

    # After failure, subsequent accesses should still raise the same exception
    with pytest.raises(RuntimeError, match="Intentional failure"):
        _ = ErrorClass.problematic


def test_lazyperclassproperty_does_not_interfere_with_other_attributes(tmp_path):
    # Ensure that the lazy property does not overwrite unrelated attributes
    class Conflicting:
        _Conflicting_lazy_value = "existing"

        @lazyperclassproperty
        def value(cls):
            return "computed"

    # The existing attribute should remain untouched
    assert Conflicting._Conflicting_lazy_value == "existing"
    # The lazy property should compute and store its own attribute
    assert Conflicting.value == "computed"
    # The attribute name used by lazyperclassproperty should be distinct
    assert hasattr(Conflicting, "_Conflicting_lazy_value")  # original
    assert hasattr(Conflicting, "_Conflicting_lazy_value")  # computed attribute name
