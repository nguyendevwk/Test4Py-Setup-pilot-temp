import pytest
from cookiecutter.repository import expand_abbreviations

def test_exact_match_expansion():
    """When the template name is an exact key, the corresponding value is returned."""
    abbreviations = {"proj": "project", "lib": "library"}
    result = expand_abbreviations("proj", abbreviations)
    assert result == "project"
    # Ensure other keys are unaffected
    assert expand_abbreviations("lib", abbreviations) == "library"

def test_prefix_with_format_expansion():
    """When the prefix matches a key, the rest of the template is formatted into the value."""
    abbreviations = {"pkg": "package-{0}", "mod": "module-{0}"}
    result = expand_abbreviations("pkg:core", abbreviations)
    assert result == "package-core"
    # Verify that the format placeholder is correctly replaced
    assert expand_abbreviations("mod:utils", abbreviations) == "module-utils"

def test_no_match_returns_original():
    """If neither the full template nor its prefix is in the abbreviations, the original template is returned."""
    abbreviations = {"foo": "bar"}
    # No exact match
    assert expand_abbreviations("baz", abbreviations) == "baz"
    # No prefix match
    assert expand_abbreviations("foo:extra", abbreviations) == "foo:extra"
