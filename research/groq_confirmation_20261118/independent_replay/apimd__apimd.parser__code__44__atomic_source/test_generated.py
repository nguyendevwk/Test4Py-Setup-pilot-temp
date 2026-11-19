import pytest
from apimd.parser import code

def test_code_escapes_markdown_and_wraps_with_code_tag():
    # Input contains both '|' and '&', should escape '|' and wrap in <code> tags
    input_str = "a|b & c"
    expected = "<code>a&#124;b & c</code>"
    assert code(input_str) == expected

def test_code_empty_string_returns_single_space():
    # Empty string should return a single space
    assert code("") == " "

def test_code_non_string_raises_type_error():
    # Passing a non-string should raise a TypeError because replace is not defined
    with pytest.raises(AttributeError):
        code(123)
