import pytest
from docstring_parser.common import DocstringDeprecated


def test_deprecated_normal():
    """Normal construction with typical values."""
    args = ["param1", "param2"]
    description = "This function is deprecated."
    version = "2.0"
    dep = DocstringDeprecated(args, description, version)
    assert dep.args == args
    assert dep.description == description
    assert dep.version == version


def test_deprecated_boundary_none():
    """Construction when optional fields are None."""
    args = []
    dep = DocstringDeprecated(args, None, None)
    assert dep.args == args
    assert dep.description is None
    assert dep.version is None


def test_deprecated_invalid_args():
    """Construction with invalid args type raises TypeError."""
    with pytest.raises(TypeError):
        DocstringDeprecated("not a list", "desc", "1.0")
