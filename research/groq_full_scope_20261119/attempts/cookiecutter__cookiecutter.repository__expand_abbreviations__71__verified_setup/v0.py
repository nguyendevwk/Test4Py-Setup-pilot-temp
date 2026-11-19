import pytest
from cookiecutter.repository import expand_abbreviations

def test_expand_full_template_match():
    abbreviations = {"proj": "myproject", "lib": "mylib"}
    # Template exactly matches a key in abbreviations
    assert expand_abbreviations("proj", abbreviations) == "myproject"

def test_expand_prefix_with_formatting():
    abbreviations = {"pkg": "package-{0}", "mod": "module-{0}"}
    # Template has a prefix that matches a key and a suffix after colon
    assert expand_abbreviations("pkg:utils", abbreviations) == "package-utils"
    assert expand_abbreviations("mod:core", abbreviations) == "module-core"

def test_expand_no_match_returns_original():
    abbreviations = {"foo": "bar"}
    # Neither the whole template nor its prefix is in abbreviations
    assert expand_abbreviations("unknown:template", abbreviations) == "unknown:template"
    assert expand_abbreviations("simple", abbreviations) == "simple"
