import abc
import pytest
from pysnooper.utils import WritableStream


class DummyWriter(WritableStream):
    def write(self, s):
        return f"written: {s}"


class NoWrite:
    pass


def test_abstract_instantiation_fails():
    """WritableStream is abstract and cannot be instantiated directly."""
    with pytest.raises(TypeError) as excinfo:
        WritableStream()
    assert "Can't instantiate abstract class" in str(excinfo.value)


def test_subclasshook_accepts_write_method():
    """A class that implements write is considered a subclass of WritableStream."""
    assert issubclass(DummyWriter, WritableStream)
    assert isinstance(DummyWriter(), WritableStream)
    assert DummyWriter().write("test") == "written: test"


def test_subclasshook_rejects_missing_write():
    """A class without a write method is not considered a subclass of WritableStream."""
    assert not issubclass(NoWrite, WritableStream)
    assert not isinstance(NoWrite(), WritableStream)
