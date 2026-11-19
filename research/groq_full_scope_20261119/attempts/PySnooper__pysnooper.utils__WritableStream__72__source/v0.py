import abc
import pytest
from pysnooper.utils import WritableStream


class DummyStream(WritableStream):
    """Concrete implementation that records written data."""
    def __init__(self):
        self.data = []

    def write(self, s):
        self.data.append(s)


def test_abstract_base_prevents_instantiation():
    """WritableStream cannot be instantiated directly."""
    with pytest.raises(TypeError):
        WritableStream()


def test_subclasshook_accepts_concrete_implementation():
    """Subclasshook should recognize a class with a write method."""
    assert issubclass(DummyStream, WritableStream)
    instance = DummyStream()
    instance.write("hello")
    assert instance.data == ["hello"]


def test_subclasshook_rejects_incomplete_class():
    """Subclasshook should reject a class missing the required method."""
    class Incomplete:
        pass

    assert not issubclass(Incomplete, WritableStream)
    with pytest.raises(TypeError):
        Incomplete()
