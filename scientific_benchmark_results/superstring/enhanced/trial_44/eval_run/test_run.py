import pytest
from superstring.superstring import SuperString, SuperStringConcatenation

def test_superstring_addition_coerces_and_concatenates():
    s1 = SuperString('Hello')
    s2 = SuperString('World')
    # Adding two SuperString instances
    s3 = s1 + s2
    assert isinstance(s3, SuperStringConcatenation)
    assert s3.length() == 10
    assert s3.to_printable() == 'HelloWorld'
    # Adding a plain string coerces it to SuperString and concatenates
    s4 = s1 + 'World'
    assert isinstance(s4, SuperStringConcatenation)
    assert s4.length() == 10
    assert s4.to_printable() == 'HelloWorld'
