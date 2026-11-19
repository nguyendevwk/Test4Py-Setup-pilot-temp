import abc
import pytest
from pysnooper.utils import WritableStream, _check_methods


class ConcreteStream(WritableStream):
    """A concrete implementation that satisfies the abstract interface."""
    def write(self, s):
        return f"written: {s}"


class IncompleteStream(WritableStream):
    """Missing the required write method; should not be instantiable."""
    pass


class NoneMethodStream(WritableStream):
    """Defines write as None; should not be considered a valid subclass."""
    write = None


def test_concrete_stream_instantiation_and_write():
    """ConcreteStream should be instantiable and its write method should work."""
    stream = ConcreteStream()
    assert isinstance(stream, WritableStream)
    result = stream.write("hello")
    assert result == "written: hello"


def test_incomplete_stream_instantiation_error():
    """Attempting to instantiate a subclass that lacks write should raise TypeError."""
    with pytest.raises(TypeError) as excinfo:
        IncompleteStream()
    assert "Can't instantiate abstract class IncompleteStream" in str(excinfo.value)


def test_none_method_stream_subclasshook():
    """A subclass that defines write as None should not be considered a subclass."""
    # The subclasshook should return NotImplemented for this case
    assert _check_methods(NoneMethodStream, 'write') is False
    # Consequently, isinstance should be False
    assert not isinstance(NoneMethodStream(), WritableStream)
