import pytest
from typesystem.fields import String

def test_string_validate_null_coercion_to_empty():
    """String.validate should coerce None to an empty string when allow_blank is True."""
    field = String(allow_blank=True)
    # Validate None: should return an empty string, not raise an error.
    assert field.validate(None) == ""
