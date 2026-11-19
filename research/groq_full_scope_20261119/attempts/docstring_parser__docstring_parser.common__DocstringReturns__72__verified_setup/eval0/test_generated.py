import pytest
from docstring_parser.common import DocstringReturns

def test_docstring_returns_basic_attributes():
    """Verify that the constructor stores the provided arguments correctly."""
    dr = DocstringReturns(
        args=["x", "y"],
        description="Returns the sum.",
        type_name="int",
        is_generator=False,
        return_name="result",
    )
    assert dr.args == ["x", "y"]
    assert dr.description == "Returns the sum."
    assert dr.type_name == "int"
    assert dr.is_generator is False
    assert dr.return_name == "result"

def test_docstring_returns_optional_parameters():
    """Verify that optional parameters default to None when omitted."""
    dr = DocstringReturns(
        args=[],
        description=None,
        type_name=None,
        is_generator=True,
    )
    assert dr.args == []
    assert dr.description is None
    assert dr.type_name is None
    assert dr.is_generator is True
    assert dr.return_name is None

def test_docstring_returns_invalid_type_name_raises():
    """Ensure that providing a non-string type_name raises a TypeError."""
    with pytest.raises(TypeError):
        # type_name should be a string or None; passing an int triggers a TypeError
        DocstringReturns(
            args=[],
            description="",
            type_name=123,  # invalid type
            is_generator=False,
        )
