import abc
import pytest
from pysnooper.utils import WritableStream


class DummyStream(WritableStream):
    """Concrete implementation of WritableStream for testing."""
    def __init__(self):
        self.contents = []

    def write(self, s):
        self.contents.append(s)


def test_abstract_instantiation_fails():
    """WritableStream cannot be instantiated directly."""
    with pytest.raises(TypeError) as excinfo:
        WritableStream()
    assert "Can't instantiate abstract class" in str(excinfo.value)
    assert "write" in str(excinfo.value)


def test_subclasshook_accepts_concrete_subclass():
    """Concrete subclass with write method is recognized as WritableStream."""
    assert issubclass(DummyStream, WritableStream)
    dummy = DummyStream()
    dummy.write("hello")
    assert dummy.contents == ["hello"]


def test_subclasshook_rejects_incomplete_subclass():
    """Class missing write method is not considered a WritableStream."""
    class IncompleteStream(abc.ABC):
        pass

    assert not issubclass(IncompleteStream, WritableStream)
    with pytest.raises(TypeError):
        IncompleteStream()
