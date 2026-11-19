import pytest
from tornado.util import Configurable, import_object

# ----------------------------------------------------------------------
# Helper classes for testing
# ----------------------------------------------------------------------
class _Base(Configurable):
    """Concrete implementation of Configurable for testing."""

    @classmethod
    def configurable_base(cls):
        return _Base

    @classmethod
    def configurable_default(cls):
        return _Base

    def initialize(self, *args, **kwargs):
        # Store initialization arguments for later inspection
        self._init_args = args
        self._init_kwargs = kwargs


class _Impl(_Base):
    """Alternative implementation used for configuration."""

    @classmethod
    def configurable_base(cls):
        return _Base

    @classmethod
    def configurable_default(cls):
        return _Base

    def initialize(self, *args, **kwargs):
        self._init_args = args
        self._init_kwargs = kwargs
        self._impl_marker = True


# ----------------------------------------------------------------------
# Test functions
# ----------------------------------------------------------------------
def test_configurable_instantiation_and_kwargs():
    """
    Verify that instantiating the base class creates an instance of the
    configured implementation and that keyword arguments are forwarded.
    """
    # Ensure no prior configuration
    _Base.configure(None)

    # Instantiate with keyword arguments
    obj = _Base(foo=1, bar=2)
    assert isinstance(obj, _Base)
    # Default implementation should be _Base itself
    assert not hasattr(obj, "_impl_marker")
    assert obj._init_kwargs == {"foo": 1, "bar": 2}
    assert obj._init_args == ()


def test_configurable_string_configuration_and_reset():
    """
    Verify that configuring with a string path works and that the
    configuration can be reset to the default.
    """
    # Configure to use the alternative implementation via string
    _Base.configure("tornado.util._Impl", extra="value")
    obj = _Base()
    assert isinstance(obj, _Impl)
    assert hasattr(obj, "_impl_marker")
    assert obj._init_kwargs == {"extra": "value"}
    assert obj._init_args == ()

    # Reset configuration to default
    _Base.configure(None)
    obj2 = _Base()
    assert isinstance(obj2, _Base)
    assert not hasattr(obj2, "_impl_marker")
    assert obj2._init_kwargs == {}
    assert obj2._init_args == ()


def test_configurable_invalid_subclass_raises():
    """
    Verify that attempting to configure with an invalid subclass raises ValueError.
    """
    class NotAConfigurable:
        pass

    with pytest.raises(ValueError) as excinfo:
        _Base.configure(NotAConfigurable)
    assert "Invalid subclass" in str(excinfo.value)
