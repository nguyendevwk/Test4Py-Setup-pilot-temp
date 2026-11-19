import pytest
from cookiecutter.repository import expand_abbreviations

def test_direct_abbreviation_expansion():
    """When the template name is an exact key in abbreviations, it should be replaced."""
    abbreviations = {"proj": "myproject", "lib": "mylibrary"}
    result = expand_abbreviations("proj", abbreviations)
    assert result == "myproject"
    # Ensure other keys are unaffected
    assert expand_abbreviations("lib", abbreviations) == "mylibrary"

def test_prefix_abbreviation_with_formatting():
    """When the prefix of the template matches an abbreviation that contains a format placeholder,
    the rest of the template should be inserted into the placeholder."""
    abbreviations = {"pkg": "package-{0}", "mod": "module-{0}"}
    result = expand_abbreviations("pkg:utils", abbreviations)
    assert result == "package-utils"
    # Test another prefix
    assert expand_abbreviations("mod:core", abbreviations) == "module-core"

def test_no_abbreviation_returns_original():
    """If the template name or its prefix is not in abbreviations, the original template should be returned."""
    abbreviations = {"foo": "bar"}
    # No colon, no match
    assert expand_abbreviations("baz", abbreviations) == "baz"
    # Colon present but prefix not in abbreviations
    assert expand_abbreviations("unknown:stuff", abbreviations) == "unknown:stuff"
