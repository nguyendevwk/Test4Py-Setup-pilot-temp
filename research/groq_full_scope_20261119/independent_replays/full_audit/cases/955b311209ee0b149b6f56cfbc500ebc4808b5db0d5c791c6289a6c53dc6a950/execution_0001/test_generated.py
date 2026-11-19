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
        self._impl_flag = True


class CustomImpl(DummyBase):
    """Custom implementation to test configuration."""

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self._custom_flag = True


def test_default_configuration(tmp_path):
    """
    Verify that the default implementation is used when no configuration
    is set and that initialization arguments are passed correctly.
    """
    # Ensure no prior configuration
    DummyBase._restore_configuration((None, {}))

    # Instantiate DummyBase; should use DummyImpl
    obj = DummyBase(1, 2, key="value")
    assert isinstance(obj, DummyImpl)
    assert getattr(obj, "_impl_flag", False) is True
    assert obj._init_args == (1, 2)
    assert obj._init_kwargs == {"key": "value"}


def test_configure_with_kwargs(tmp_path):
    """
    Test that configuring a subclass with keyword arguments stores
    those arguments and passes them to the constructor.
    """
    # Configure DummyBase to use CustomImpl with a default kwarg
    DummyBase.configure(CustomImpl, default="yes")

    # Instantiate DummyBase; should use CustomImpl and include default kwarg
    obj = DummyBase(3, 4, extra="data")
    assert isinstance(obj, CustomImpl)
    assert getattr(obj, "_custom_flag", False) is True
    # The default kwarg should be merged with the explicit one
    assert obj._init_kwargs == {"default": "yes", "extra": "data"}
    assert obj._init_args == (3, 4)

    # Clean up configuration for other tests
    DummyBase._restore_configuration((None, {}))


def test_invalid_configuration_raises(tmp_path):
    """
    Verify that configuring with an invalid subclass raises ValueError.
    """
    class NotAConfigurable:
        pass

    with pytest.raises(ValueError, match="Invalid subclass"):
        DummyBase.configure(NotAConfigurable)
