import pytest
from docstring_parser.common import DocstringReturns


def test_docstring_returns_basic_attributes():
    """Verify that basic attributes are stored correctly."""
    dr = DocstringReturns(
        args=["x", "y"],
        description="Return the sum.",
        type_name="int",
        is_generator=False,
        return_name="result",
    )
    assert dr.args == ["x", "y"]
    assert dr.description == "Return the sum."
    assert dr.type_name == "int"
    assert dr.is_generator is False
    assert dr.return_name == "result"


def test_docstring_returns_optional_fields():
    """Verify that optional fields can be omitted and default to None."""
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


def test_docstring_returns_invalid_input_raises():
    """Passing non-list to args should raise a TypeError."""
    with pytest.raises(TypeError):
        DocstringReturns(
            args="not a list",
            description="Invalid args type",
            type_name="str",
            is_generator=False,
        )
