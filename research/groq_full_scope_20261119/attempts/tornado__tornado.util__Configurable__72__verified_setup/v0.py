import pytest
from types import SimpleNamespace

# Import the target module
from tornado.util import Configurable


class DummyBase(Configurable):
    """Concrete implementation of Configurable for testing."""

    @classmethod
    def configurable_base(cls):
        return DummyBase

    @classmethod
    def configurable_default(cls):
        return DummyBase

    def initialize(self, *args, **kwargs):
        # Store initialization arguments for verification
        self._init_args = args
        self._init_kwargs = kwargs


class DummyImpl(DummyBase):
    """Alternative implementation used for configuration."""

    @classmethod
    def configurable_base(cls):
        return DummyBase

    @classmethod
    def configurable_default(cls):
        return DummyBase

    def initialize(self, *args, **kwargs):
        self._init_args = args
        self._init_kwargs = kwargs
        self._impl_marker = True


def test_default_initialization():
    """Instantiating without configuration uses the default class."""
    obj = DummyBase()
    assert isinstance(obj, DummyBase)
    assert not hasattr(obj, "_impl_marker")
    assert obj._init_args == ()
    assert obj._init_kwargs == {}


def test_configure_with_kwargs_and_impl(tmp_path):
    """Configure a subclass with additional keyword arguments."""
    # Save original configuration to restore later
    original = DummyBase._save_configuration()
    try:
        DummyBase.configure(DummyImpl, foo="bar", path=str(tmp_path))
        obj = DummyBase()
        # The instance should be of the configured implementation
        assert isinstance(obj, DummyImpl)
        # Keyword arguments should be merged
        assert obj._init_kwargs["foo"] == "bar"
        assert obj._init_kwargs["path"] == str(tmp_path)
        # No positional args were passed
        assert obj._init_args == ()
        # The implementation marker should be set
        assert getattr(obj, "_impl_marker", False)
    finally:
        DummyBase._restore_configuration(original)


def test_invalid_configuration_raises():
    """Providing an invalid subclass to configure raises ValueError."""
    class NotADummy:
        pass

    with pytest.raises(ValueError, match="Invalid subclass"):
        DummyBase.configure(NotADummy)
