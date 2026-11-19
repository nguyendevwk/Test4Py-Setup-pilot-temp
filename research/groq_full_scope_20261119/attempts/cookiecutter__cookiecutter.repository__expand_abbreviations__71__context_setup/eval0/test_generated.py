import pytest
from cookiecutter.repository import expand_abbreviations

def test_exact_match_replaces_template():
    abbreviations = {"proj": "my_project"}
    result = expand_abbreviations("proj", abbreviations)
    assert result == "my_project"

def test_prefix_match_formats_rest():
    abbreviations = {"lib:": "library_{0}"}
    result = expand_abbreviations("lib:utils", abbreviations)
    assert result == "library_utils"

def test_no_match_returns_original():
    abbreviations = {"foo": "bar"}
    result = expand_abbreviations("unknown:template", abbreviations)
    assert result == "unknown:template"
