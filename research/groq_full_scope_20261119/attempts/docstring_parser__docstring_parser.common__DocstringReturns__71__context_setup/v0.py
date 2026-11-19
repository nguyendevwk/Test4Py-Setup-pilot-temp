import pytest
from docstring_parser.common import DocstringReturns, DocstringMeta


def test_docstring_returns_basic_initialization():
    """Verify that DocstringReturns correctly stores basic attributes."""
    dr = DocstringReturns(
        args=["x", "y"],
        description="Returns the sum.",
        type_name="int",
        is_generator=False,
        return_name="result",
    )
    assert isinstance(dr, DocstringMeta)
    assert dr.args == ["x", "y"]
    assert dr.description == "Returns the sum."
    assert dr.type_name == "int"
    assert dr.is_generator is False
    assert dr.return_name == "result"


def test_docstring_returns_boundary_values():
    """Test initialization with boundary values such as empty lists and None."""
    dr = DocstringReturns(
        args=[],
        description=None,
        type_name=None,
        is_generator=True,
        return_name=None,
    )
    assert dr.args == []
    assert dr.description is None
    assert dr.type_name is None
    assert dr.is_generator is True
    assert dr.return_name is None


def test_docstring_returns_attribute_mutation_and_type():
    """Ensure attributes can be mutated and retain correct types."""
    dr = DocstringReturns(
        args=["a"],
        description="desc",
        type_name="str",
        is_generator=False,
    )
    # Mutate attributes
    dr.args.append("b")
    dr.description = "new desc"
    dr.type_name = "bytes"
    dr.is_generator = True
    dr.return_name = "output"

    assert dr.args == ["a", "b"]
    assert dr.description == "new desc"
    assert dr.type_name == "bytes"
    assert dr.is_generator is True
    assert dr.return_name == "output"
