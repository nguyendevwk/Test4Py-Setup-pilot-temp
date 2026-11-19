from docstring_parser.numpydoc import parse
from docstring_parser.common import Docstring
import textwrap

def test_parse_numpydoc_sections_and_content():
    docstring = textwrap.dedent("""\
        Summary.

        Parameters
        ----------
        x : int
            Param x.

        Returns
        -------
        int
            Return value.

        Raises
        ------
        ValueError
            Error description.

        Examples
        --------
        >>> result = func(1)
        >>> assert result == 1
    """)
    doc = parse(docstring)
    assert isinstance(doc, Docstring)
    assert doc.short_description == "Summary."
    assert len(doc.params) == 1
    param = doc.params[0]
    assert (param.arg_name, param.type_name, param.description) == ("x", "int", "Param x.")
    assert len(doc.returns) == 1
    ret = doc.returns[0]
    assert (ret.type_name, ret.description) == ("int", "Return value.")
    assert len(doc.raises) == 1
    raise_ = doc.raises[0]
    assert (raise_.type_name, raise_.description) == ("ValueError", "Error description.")
    assert len(doc.examples) == 1
    assert ">>> result = func(1)" in doc.examples[0]
    assert not any([doc.attributes, doc.methods, doc.others, doc.warnings, doc.extends, doc.etc])
