import abc
import pytest
from pysnooper.utils import WritableStream, _check_methods


class ConcreteStream(WritableStream):
    def write(self, s):
        return f"written: {s}"


class IncompleteStream(WritableStream):
    pass


def test_writable_stream_subclasshook_true():
    """ConcreteStream should be recognized as a WritableStream."""
    assert isinstance(ConcreteStream(), WritableStream)
    assert issubclass(ConcreteStream, WritableStream)
    # The subclasshook should return True for ConcreteStream
    assert WritableStream.__subclasshook__(ConcreteStream) is True


def test_writable_stream_subclasshook_false():
    """IncompleteStream should not be recognized as a WritableStream."""
    assert not isinstance(IncompleteStream(), WritableStream)
    assert not issubclass(IncompleteStream, WritableStream)
    # The subclasshook should return NotImplemented for IncompleteStream
    assert WritableStream.__subclasshook__(IncompleteStream) is NotImplemented


def test_abstract_write_method_prevents_instantiation():
    """Attempting to instantiate a subclass without implementing write should raise TypeError."""
    with pytest.raises(TypeError):
        IncompleteStream()
