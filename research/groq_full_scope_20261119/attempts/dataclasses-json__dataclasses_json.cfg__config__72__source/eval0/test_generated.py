import pytest
from dataclasses_json.cfg import config, Undefined, UndefinedParameterError
from marshmallow.fields import Integer

def test_config_basic_metadata_and_mm_field():
    """Verify that encoder, decoder, and mm_field are stored correctly."""
    def encoder(x): return str(x)
    def decoder(x): return int(x)

    meta = config(
        metadata={'foo': 'bar'},
        encoder=encoder,
        decoder=decoder,
        mm_field=Integer()
    )
    # The original metadata dict should be preserved
    assert meta['foo'] == 'bar'
    # The dataclasses_json sub-dict should contain the provided values
    sub = meta['dataclasses_json']
    assert sub['encoder'] is encoder
    assert sub['decoder'] is decoder
    assert isinstance(sub['mm_field'], Integer)

def test_config_letter_case_override():
    """Verify that field_name overrides letter_case correctly."""
    def custom_case(name): return name.upper()
    meta = config(
        field_name='my_field',
        letter_case=custom_case
    )
    # The letter_case function should now return the overridden name
    letter_case_func = meta['dataclasses_json']['letter_case']
    assert letter_case_func(None, 'ignored') == 'MY_FIELD'

def test_config_invalid_undefined_raises():
    """Verify that an invalid undefined action raises UndefinedParameterError."""
    with pytest.raises(UndefinedParameterError) as excinfo:
        config(undefined='nonexistent')
    # The error message should list valid actions
    valid_actions = [action.name for action in Undefined]
    assert all(action in str(excinfo.value) for action in valid_actions)
