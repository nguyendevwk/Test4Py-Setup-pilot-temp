import pytest
from docstring_parser.common import DocstringDeprecated


def test_deprecated_initialization_with_full_data():
    """DocstringDeprecated should store all provided values correctly."""
    args = ["arg1", "arg2"]
    description = "This function is deprecated."
    version = "2.0"
    dep = DocstringDeprecated(args, description, version)

    # Assert that the attributes are set as expected
    assert dep.args == args
    assert dep.description == description
    assert dep.version == version


def test_deprecated_initialization_with_empty_args_and_no_description():
    """DocstringDeprecated should handle empty args list and None description."""
    args = []
    description = None
    version = "1.5"
    dep = DocstringDeprecated(args, description, version)

    # The args list should be empty
    assert dep.args == args
    # The description should be None
    assert dep.description is None
    # The version should still be set
    assert dep.version == version


def test_deprecated_initialization_with_invalid_args_type():
    """Passing a non-list to args should raise a TypeError due to type mismatch."""
    with pytest.raises(TypeError):
        # The constructor expects a list; passing a string should trigger a TypeError
        DocstringDeprecated("not-a-list", "desc", "1.0")
