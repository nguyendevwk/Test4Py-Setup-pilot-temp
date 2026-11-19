import pytest
from docstring_parser.common import DocstringReturns

def test_docstring_returns_basic_attributes():
    """Verify that the constructor correctly assigns basic attributes."""
    dr = DocstringReturns(
        args=["x", "y"],
        description="Return the sum of x and y.",
        type_name="int",
        is_generator=False,
    )
    assert dr.args == ["x", "y"]
    assert dr.description == "Return the sum of x and y."
    assert dr.type_name == "int"
    assert dr.is_generator is False
    assert dr.return_name is None

def test_docstring_returns_with_return_name_and_generator():
    """Verify that optional return_name and is_generator flag are stored."""
    dr = DocstringReturns(
        args=[],
        description=None,
        type_name=None,
        is_generator=True,
        return_name="value",
    )
    assert dr.args == []
    assert dr.description is None
    assert dr.type_name is None
    assert dr.is_generator is True
    assert dr.return_name == "value"

def test_docstring_returns_invalid_args_type():
    """Passing a non-list to args should raise a TypeError."""
    with pytest.raises(TypeError):
        # args must be a list; passing a string should trigger a TypeError
        DocstringReturns(
            args="not a list",
            description="",
            type_name="",
            is_generator=False,
        )
