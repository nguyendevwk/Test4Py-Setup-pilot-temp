import pytest
import types
from tornado.util import Configurable, import_object


class DummyBase(Configurable):
    """A minimal concrete implementation of Configurable for testing."""

    @classmethod
    def configurable_base(cls):
        return cls

    @classmethod
    def configurable_default(cls):
        return DummyImpl

    def initialize(self, *args, **kwargs):
        # store initialization data for assertions
        self._init_args = args
        self._init_kwargs = kwargs


class DummyImpl(DummyBase):
    """Concrete implementation used by default."""

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self._impl_marker = True


class AlternateImpl(DummyBase):
    """Alternate implementation used when configured."""

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self._impl_marker = False


def test_configure_with_class_and_kwargs(tmp_path):
    # Ensure default implementation is used initially
    instance = DummyBase()
    assert isinstance(instance, DummyImpl)
    assert instance._impl_marker is True
    assert instance._init_kwargs == {}

    # Configure to use AlternateImpl with a keyword argument
    DummyBase.configure(AlternateImpl, foo="bar")
    instance2 = DummyBase()
    assert isinstance(instance2, AlternateImpl)
    assert instance2._impl_marker is False
    assert instance2._init_kwargs["foo"] == "bar"

    # Clean up configuration for other tests
    DummyBase.configure(None)


def test_configure_with_string_import_and_error():
    # Importing a valid class by string should work
    DummyBase.configure("tornado.util.AlternateImpl")
    instance = DummyBase()
    assert isinstance(instance, AlternateImpl)
    DummyBase.configure(None)

    # Importing a non‑existent module should raise ImportError
    with pytest.raises(ImportError):
        DummyBase.configure("tornado.util.nonexistent_module")

    # Importing a non‑existent attribute should raise ImportError
    with pytest.raises(ImportError):
        DummyBase.configure("tornado.util.NonExistentClass")

    # Importing a valid module but wrong type should raise ValueError
    with pytest.raises(ValueError):
        DummyBase.configure("tornado.util.types")  # types module is not a subclass


def test_invalid_subclass_configuration():
    # Attempt to configure with an unrelated class should raise ValueError
    class Unrelated:
        pass

    with pytest.raises(ValueError):
        DummyBase.configure(Unrelated)

    # Attempt to configure with a subclass that does not inherit from DummyBase
    class NotDerived(DummyBase):
        pass

    # This should be allowed because it is a subclass of DummyBase
    DummyBase.configure(NotDerived)
    instance = DummyBase()
    assert isinstance(instance, NotDerived)
    DummyBase.configure(None)
