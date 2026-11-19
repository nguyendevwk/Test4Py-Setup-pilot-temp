import pytest
from docstring_parser.common import (
    Docstring,
    DocstringParam,
    DocstringRaises,
    DocstringReturns,
    DocstringDeprecated,
    DocstringExample,
)

def test_description_construction_and_blank_handling():
    d = Docstring()
    # No description yet
    assert d.description is None

    # Set short and long descriptions with blank flags
    d.short_description = "Short"
    d.long_description = "Long"
    d.blank_after_short_description = True
    d.blank_after_long_description = False

    # Expected: short, blank line, long
    expected = "Short\n\nLong"
    assert d.description == expected

    # Remove short description
    d.short_description = None
    assert d.description == "Long"

    # Remove long description
    d.long_description = None
    assert d.description is None

def test_meta_filters_and_multiple_returns():
    d = Docstring()
    # Add various meta items
    d.meta.extend([
        DocstringParam(args=["arg1"], description="desc1", arg_name="a", type_name="int", is_optional=False, default=None),
        DocstringParam(args=["arg2"], description="desc2", arg_name="b", type_name="str", is_optional=True, default="'x'"),
        DocstringRaises(args=["ValueError"], description="bad", type_name="ValueError"),
        DocstringReturns(args=["return"], description="result", type_name="int", is_generator=False),
        DocstringReturns(args=["return2"], description="another", type_name="str", is_generator=True, return_name="y"),
        DocstringDeprecated(args=["deprecated"], description="old", version="1.0"),
        DocstringExample(args=["example"], snippet="print('hi')", description="greeting"),
    ])

    # params should return only DocstringParam instances
    params = d.params
    assert len(params) == 2
    assert all(isinstance(p, DocstringParam) for p in params)
    assert [p.arg_name for p in params] == ["a", "b"]

    # raises should return only DocstringRaises instances
    raises = d.raises
    assert len(raises) == 1
    assert isinstance(raises[0], DocstringRaises)
    assert raises[0].type_name == "ValueError"

    # returns should return the first DocstringReturns
    first_return = d.returns
    assert isinstance(first_return, DocstringReturns)
    assert first_return.type_name == "int"

    # many_returns should return all DocstringReturns
    many = d.many_returns
    assert len(many) == 2
    assert [r.type_name for r in many] == ["int", "str"]

    # deprecation should return the first DocstringDeprecated
    dep = d.deprecation
    assert isinstance(dep, DocstringDeprecated)
    assert dep.version == "1.0"

    # examples should return all DocstringExample
    exs = d.examples
    assert len(exs) == 1
    assert isinstance(exs[0], DocstringExample)
    assert exs[0].snippet == "print('hi')"

def test_edge_cases_and_type_consistency():
    d = Docstring()
    # Empty meta list should yield None or empty lists appropriately
    assert d.params == []
    assert d.raises == []
    assert d.returns is None
    assert d.many_returns == []
    assert d.deprecation is None
    assert d.examples == []

    # Adding a meta item of an unrelated type should not affect filters
    class DummyMeta:
        pass
    d.meta.append(DummyMeta())
    assert d.params == []
    assert d.raises == []
    assert d.returns is None
    assert d.many_returns == []
    assert d.deprecation is None
    assert d.examples == []
