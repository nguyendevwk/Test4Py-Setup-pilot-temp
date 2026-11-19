import pytest
from types import SimpleNamespace

# Import the target class
from tornado.util import Configurable


class DummyBase(Configurable):
    """Concrete implementation of Configurable for testing."""

    @classmethod
    def configurable_base(cls):
        return DummyBase

    @classmethod
    def configurable_default(cls):
        return DummyImpl

    def initialize(self, *args, **kwargs):
        # Store initialization arguments for inspection
        self._init_args = args
        self._init_kwargs = kwargs


class DummyImpl(DummyBase):
    """Implementation subclass used by default."""

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self._impl_marker = "impl"


class AnotherImpl(DummyBase):
    """Alternative implementation for configuration tests."""

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self._impl_marker = "another"


def test_default_implementation_and_initialization(tmp_path):
    """Instantiating the base class uses the default implementation."""
    # Ensure no prior configuration
    DummyBase._restore_configuration((None, {}))
    instance = DummyBase()
    # The instance should be of the default implementation class
    assert isinstance(instance, DummyImpl)
    # The initialize method should have been called with no args
    assert instance._init_args == ()
    assert instance._init_kwargs == {}
    # Implementation marker set by DummyImpl
    assert getattr(instance, "_impl_marker", None) == "impl"


def test_configure_with_kwargs_and_subclass(tmp_path):
    """Configuring the base class with a subclass and kwargs."""
    # Save current configuration to restore later
    saved = DummyBase._save_configuration()
    try:
        # Configure to use AnotherImpl with a keyword argument
        DummyBase.configure(AnotherImpl, foo="bar")
        instance = DummyBase()
        # Instance should be of the configured subclass
        assert isinstance(instance, AnotherImpl)
        # The keyword argument should be passed to initialize
        assert instance._init_kwargs == {"foo": "bar"}
        # Implementation marker set by AnotherImpl
        assert getattr(instance, "_impl_marker", None) == "another"
    finally:
        # Restore original configuration
        DummyBase._restore_configuration(saved)


def test_invalid_configuration_raises_value_error(tmp_path):
    """Providing an invalid subclass to configure raises ValueError."""
    # Attempt to configure with a class that is not a subclass of DummyBase
    class NotSub:
        pass

    with pytest.raises(ValueError, match="Invalid subclass"):
        DummyBase.configure(NotSub)
