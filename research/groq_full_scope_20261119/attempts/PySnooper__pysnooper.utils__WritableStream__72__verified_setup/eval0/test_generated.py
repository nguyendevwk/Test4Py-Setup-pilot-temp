import abc
import pytest
from pysnooper.utils import WritableStream


class ConcreteStream(WritableStream):
    """A minimal concrete implementation of WritableStream."""
    def write(self, s):
        # simply store the last written value for inspection
        self.last = s


def test_concrete_implementation_is_instance():
    """ConcreteStream should be an instance of WritableStream."""
    stream = ConcreteStream()
    assert isinstance(stream, WritableStream)
    # The write method should be callable and store the value
    stream.write("hello")
    assert stream.last == "hello"


def test_subclass_without_write_is_abstract():
    """A subclass missing the write method should remain abstract."""
    class IncompleteStream(WritableStream):
        pass

    # The subclass should still be abstract because write is not implemented
    assert abc.isabstract(IncompleteStream)
    with pytest.raises(TypeError):
        IncompleteStream()  # cannot instantiate abstract class


def test_subclasshook_accepts_any_with_write():
    """Any class that defines a write method should satisfy WritableStream."""
    class Dummy:
        def write(self, s):
            pass

    # The subclasshook should return True for Dummy
    assert WritableStream.__subclasshook__(Dummy) is True
    # And Dummy should be considered a subclass
    assert issubclass(Dummy, WritableStream)
