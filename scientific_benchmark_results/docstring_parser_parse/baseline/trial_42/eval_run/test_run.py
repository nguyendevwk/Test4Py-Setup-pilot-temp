import pytest
from docstring_parser.parser import parse, google
from docstring_parser._sections import SectionSpec
from docstring_parser.common import Kind

def test_parse_raises_value_error_when_sections_provided_with_parser():
    # A parser instance (google) is passed with a non‑None sections argument.
    # According to the implementation, this should raise a ValueError.
    sections = [SectionSpec(titles="Example", kind=Kind.PARAM)]
    with pytest.raises(ValueError):
        parse("Some docstring", style=google, sections=sections)
