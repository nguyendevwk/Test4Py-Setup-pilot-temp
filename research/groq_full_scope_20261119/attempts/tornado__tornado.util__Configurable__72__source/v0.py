import pytest
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


def test_configurable_default_instantiation():
    """Instantiating without configuration should use the default class."""
    # Ensure no prior configuration
    DummyBase._restore_configuration((None, {}))
    instance = DummyBase()
    assert isinstance(instance, DummyBase)
    assert not hasattr(instance, "_impl_marker")
    assert instance._init_args == ()
    assert instance._init_kwargs == {}


def test_configurable_configure_and_kwargs(tmp_path):
    """Configuring with an implementation and kwargs should affect instantiation."""
    # Save current configuration to restore later
    saved = DummyBase._save_configuration()
    try:
        DummyBase.configure(DummyImpl, foo="bar", path=str(tmp_path))
        instance = DummyBase()
        assert isinstance(instance, DummyImpl)
        assert hasattr(instance, "_impl_marker")
        # kwargs passed to configure should be merged with constructor kwargs
        assert instance._init_kwargs["foo"] == "bar"
        assert instance._init_kwargs["path"] == str(tmp_path)
    finally:
        DummyBase._restore_configuration(saved)


def test_configurable_invalid_subclass_raises():
    """Passing an invalid subclass to configure should raise ValueError."""
    class NotADummy:
        pass

    with pytest.raises(ValueError, match="Invalid subclass"):
        DummyBase.configure(NotADummy)
