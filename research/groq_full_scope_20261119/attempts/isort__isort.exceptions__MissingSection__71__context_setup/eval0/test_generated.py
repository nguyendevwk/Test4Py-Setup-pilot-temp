import pytest
from isort.exceptions import MissingSection, ISortError


def test_missing_section_message_contains_details():
    """The error message should include the import module and section names."""
    exc = MissingSection(import_module="my.module", section="CUSTOM")
    expected_substring = "Found my.module import while parsing, but CUSTOM was not included"
    assert expected_substring in str(exc)


def test_missing_section_inherits_from_isort_error_and_exception():
    """MissingSection must be a subclass of ISortError and Exception."""
    exc = MissingSection(import_module="x", section="y")
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)


def test_missing_section_reduce_roundtrip(tmp_path):
    """The __reduce__ method should allow the exception to be pickled and unpickled."""
    import pickle
    exc = MissingSection(import_module="pkg.mod", section="SECTION")
    data = pickle.dumps(exc)
    loaded = pickle.loads(data)
    assert isinstance(loaded, MissingSection)
    assert str(loaded) == str(exc)
