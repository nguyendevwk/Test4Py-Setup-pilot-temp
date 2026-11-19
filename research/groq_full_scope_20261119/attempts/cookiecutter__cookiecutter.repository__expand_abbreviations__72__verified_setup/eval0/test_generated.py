import pytest
from cookiecutter.repository import expand_abbreviations

def test_exact_match_expansion():
    abbreviations = {"proj": "myproject", "lib": "mylib"}
    assert expand_abbreviations("proj", abbreviations) == "myproject"
    assert expand_abbreviations("lib", abbreviations) == "mylib"

def test_prefix_expansion_with_format():
    abbreviations = {"pkg": "package-{0}", "mod": "module-{0}-v1"}
    # The part after the colon should be inserted into the format string
    assert expand_abbreviations("pkg:core", abbreviations) == "package-core"
    assert expand_abbreviations("mod:utils", abbreviations) == "module-utils-v1"

def test_no_match_returns_original():
    abbreviations = {"foo": "bar"}
    # No abbreviation matches the whole template or its prefix
    assert expand_abbreviations("unknown", abbreviations) == "unknown"
    assert expand_abbreviations("unknown:part", abbreviations) == "unknown:part"
