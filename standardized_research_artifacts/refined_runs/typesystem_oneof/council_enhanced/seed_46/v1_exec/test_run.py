import pytest
from typesystem.composites import OneOf
from typesystem.fields import String, Integer

def test_oneof_exactly_one_match_and_error_cases():
    # Exactly one match: string value
    schema_str = OneOf([String(), Integer()])
    val, err = schema_str.validate_or_error('sample_text')
    assert err is None
    assert val == 'sample_text'

    # Exactly one match: integer value
    val, err = schema_str.validate_or_error(42)
    assert err is None
    assert val == 42

    # No match: value that fails both (None)
    val, err = schema_str.validate_or_error(None)
    assert val is None
    assert err is not None
    assert err.code == 'no_match'

    # Multiple matches: two identical String fields both accept the value
    schema_multi = OneOf([String(), String()])
    with pytest.raises(Exception) as excinfo:
        schema_multi.validate('duplicate')
    # The raised exception should be a ValidationError with code 'multiple_matches'
    assert hasattr(excinfo.value, 'code')
    assert excinfo.value.code == 'multiple_matches'
