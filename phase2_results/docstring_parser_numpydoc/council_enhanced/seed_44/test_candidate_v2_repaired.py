import pytest
from docstring_parser.numpydoc import parse
from docstring_parser.common import DocstringParam, DocstringReturns

def test_parse_numpydoc_sections_and_description():
    text = """Short summary line.

    Long description that spans
    multiple lines.

    Parameters
    ----------
    param1 : int
        The first parameter.
    param2 : str, optional
        The second parameter.

    Returns
    -------
    bool
        True if successful.
    """
    doc = parse(text)
    assert doc.style.name == "NUMPY"
    assert doc.short_description == "Short summary line."
    assert doc.long_description == "Long description that spans\nmultiple lines."
    assert doc.blank_after_short_description is False
    assert doc.blank_after_long_description is False

    assert len(doc.params) == 2
    names = {p.arg_name for p in doc.params}
    assert names == {"param1", "param2"}
    param1 = doc.params_by_name["param1"]
    assert isinstance(param1, DocstringParam)
    assert param1.type_name == "int"
    assert param1.description == "The first parameter."

    returns = [m for m in doc.meta if isinstance(m, DocstringReturns)]
    assert len(returns) == 1
    assert returns[0].type_name == "bool"
    assert returns[0].description == "True if successful."

    doc_no_sections = parse(text, sections=[])
    assert doc_no_sections.params == []
    assert doc_no_sections.meta == []

    doc_none = parse(None)
    assert doc_none.description is None
    assert doc_none.params == []
    assert doc_none.meta == []

    doc_empty = parse("")
    assert doc_empty.description is None
    assert doc_empty.params == []
    assert doc_empty.meta == []
