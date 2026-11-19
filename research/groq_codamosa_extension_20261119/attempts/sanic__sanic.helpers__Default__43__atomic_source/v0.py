import pytest
from sanic.helpers import Default


def test_repr_and_str():
    """Default should have a consistent string representation."""
    d = Default()
    assert repr(d) == "<Default>"
    assert str(d) == "<Default>"
    # repr and str should be identical
    assert repr(d) == str(d)


def test_identity_and_equality():
    """Each Default instance is unique; they are not equal to each other."""
    d1 = Default()
    d2 = Default()
    assert d1 is not d2
    # Equality is identity-based; different instances are not equal
    assert d1 != d2
    # A Default instance is not equal to None or object()
    assert d1 != None
    assert d1 != object()


def test_default_as_function_parameter(tmp_path):
    """Default can be used as a sentinel for function arguments."""
    sentinel = Default()

    def write_if_not_default(path: str, content: str = sentinel):
        """Write content to a file only if a non-sentinel value is provided."""
        if content is sentinel:
            return False
        with open(path, "w") as f:
            f.write(content)
        return True

    file_path = tmp_path / "test.txt"

    # When the sentinel is used, nothing is written
    assert write_if_not_default(str(file_path)) is False
    assert not file_path.exists()

    # When a real string is provided, the file is created and written
    assert write_if_not_default(str(file_path), "hello") is True
    assert file_path.read_text() == "hello"
