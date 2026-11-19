import pytest
from docstring_parser.common import (
    Docstring,
    DocstringParam,
    DocstringRaises,
    DocstringReturns,
    DocstringDeprecated,
    DocstringExample,
)

def test_description_with_blank_and_long():
    """Test that description concatenates short, optional blank, and long parts."""
    d = Docstring()
    d.short_description = "Short"
    d.blank_after_short_description = True
    d.long_description = "Long description."
    assert d.description == "Short\n\nLong description."

def test_meta_properties_and_order():
    """Test that meta items are correctly exposed via the various properties."""
    d = Docstring()
    d.meta = [
        DocstringParam(["arg"], "desc", "arg", "int", False, None),
        DocstringRaises(["exc"], "error", "ValueError"),
        DocstringReturns(["ret"], "result", "str", False, None),
        DocstringDeprecated(["deprecated"], "use new", "1.2"),
        DocstringExample(["ex"], "print(1)", "example"),
        DocstringReturns(["ret2"], "second", "int", False, None),
    ]

    # params
    params = d.params
    assert len(params) == 1
    assert isinstance(params[0], DocstringParam)
    assert params[0].arg_name == "arg"

    # raises
    raises = d.raises
    assert len(raises) == 1
    assert isinstance(raises[0], DocstringRaises)
    assert raises[0].type_name == "ValueError"

    # returns (first only)
    returns = d.returns
    assert isinstance(returns, DocstringReturns)
    assert returns.return_name is None

    # many_returns
    many = d.many_returns
    assert len(many) == 2
    assert all(isinstance(r, DocstringReturns) for r in many)

    # deprecation
    dep = d.deprecation
    assert isinstance(dep, DocstringDeprecated)
    assert dep.version == "1.2"

    # examples
    exs = d.examples
    assert len(exs) == 1
    assert isinstance(exs[0], DocstringExample)
    assert exs[0].snippet == "print(1)"

def test_description_none_when_no_parts():
    """Test that description property returns None when no parts are set."""
    d = Docstring()
    assert d.description is None
