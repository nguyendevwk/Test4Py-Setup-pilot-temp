import pytest
from docstring_parser.rest import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns, Kind


def test_parse_rest_docstring_parses_meta_entries():
    text = ":param name: param desc\n:type name: str\n:returns: return desc"
    doc = parse(text)

    assert isinstance(doc, Docstring)
    assert doc.short_description is None
    assert doc.long_description is None
    assert doc.description is None

    assert len(doc.meta) == 3

    param_meta = next(
        (m for m in doc.meta if isinstance(m, DocstringParam) and m.kind is Kind.PARAM),
        None,
    )
    assert param_meta is not None
    assert param_meta.arg_name == "name"
    assert param_meta.description == "param desc"

    type_meta = next(
        (m for m in doc.meta if isinstance(m, DocstringParam) and m.kind is Kind.TYPE),
        None,
    )
    assert type_meta is not None
    assert type_meta.arg_name == "name"
    assert type_meta.type_name == "str"

    return_meta = next((m for m in doc.meta if isinstance(m, DocstringReturns)), None)
    assert return_meta is not None
    assert return_meta.description == "return desc"
