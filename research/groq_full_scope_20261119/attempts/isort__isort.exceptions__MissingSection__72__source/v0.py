import pytest
from isort.exceptions import MissingSection

def test_missing_section_message_contains_import_and_section():
    exc = MissingSection("my.module", "CUSTOM")
    msg = str(exc)
    assert "my.module" in msg
    assert "CUSTOM" in msg
    assert "Found my.module import while parsing" in msg
    assert "CUSTOM was not included" in msg

def test_missing_section_message_is_deterministic():
    exc1 = MissingSection("a.b", "SEC1")
    exc2 = MissingSection("a.b", "SEC1")
    assert str(exc1) == str(exc2)

def test_missing_section_inherits_from_ISortError():
    exc = MissingSection("x.y", "SEC2")
    # ISortError is the base class for all isort exceptions
    from isort.exceptions import ISortError
    assert isinstance(exc, ISortError)
