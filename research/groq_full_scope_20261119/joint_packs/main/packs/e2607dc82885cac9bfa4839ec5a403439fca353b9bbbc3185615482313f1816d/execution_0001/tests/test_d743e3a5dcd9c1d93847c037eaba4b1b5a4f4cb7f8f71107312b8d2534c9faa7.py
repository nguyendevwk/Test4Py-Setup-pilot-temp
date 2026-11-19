import pytest
from docstring_parser.common import DocstringReturns, DocstringMeta

def test_docstring_returns_basic_initialization():
    """Verify that a DocstringReturns instance stores all provided attributes."""
    dr = DocstringReturns(
        args=["x", "y"],
        description="Returns the sum.",
        type_name="int",
        is_generator=False,
        return_name="result",
    )
    # Base class attributes
    assert isinstance(dr, DocstringMeta)
    assert dr.args == ["x", "y"]
    assert dr.description == "Returns the sum."
    # Specific attributes
    assert dr.type_name == "int"
    assert dr.is_generator is False
    assert dr.return_name == "result"

def test_docstring_returns_with_minimal_arguments():
    """Test initialization with minimal and optional arguments omitted."""
    dr = DocstringReturns(
        args=[],
        description=None,
        type_name=None,
        is_generator=True,
    )
    # Base class attributes
    assert dr.args == []
    assert dr.description is None
    # Specific attributes
    assert dr.type_name is None
    assert dr.is_generator is True
    assert dr.return_name is None

def test_docstring_returns_attribute_mutation_and_type_consistency():
    """Ensure that attributes can be mutated and retain correct types."""
    dr = DocstringReturns(
        args=["a"],
        description="Single return.",
        type_name="str",
        is_generator=False,
    )
    # Mutate attributes
    dr.args.append("b")
    dr.description = "Updated description."
    dr.type_name = "bytes"
    dr.is_generator = True
    dr.return_name = "output"
    # Assertions after mutation
    assert dr.args == ["a", "b"]
    assert dr.description == "Updated description."
    assert dr.type_name == "bytes"
    assert dr.is_generator is True
    assert dr.return_name == "output"
