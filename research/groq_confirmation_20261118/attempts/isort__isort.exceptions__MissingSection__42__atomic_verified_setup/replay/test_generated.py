import pytest
from isort.exceptions import MissingSection, ISortError


def test_missing_section_message_contains_details(tmp_path):
    """The exception message should include the import module and section names."""
    exc = MissingSection(import_module="my.module", section="CUSTOM")
    assert "my.module" in str(exc)
    assert "CUSTOM" in str(exc)
    assert "Found my.module import while parsing" in str(exc)
    assert "CUSTOM was not included" in str(exc)


def test_missing_section_with_empty_strings(tmp_path):
    """Providing empty strings should still produce a coherent message."""
    exc = MissingSection(import_module="", section="")
    msg = str(exc)
    assert "Found  import while parsing" in msg
    assert "was not included" in msg
    # Ensure the message is not empty
    assert len(msg) > 0


def test_missing_section_is_subclass_of_isort_error(tmp_path):
    """MissingSection should be an instance of ISortError."""
    exc = MissingSection(import_module="foo", section="bar")
    assert isinstance(exc, ISortError)
    # Also check that it behaves like a normal exception
    with pytest.raises(MissingSection) as cm:
        raise exc
    assert cm.value is exc
