import pytest
from dataclasses_json.cfg import config, LetterCase
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.fields import Field as MarshmallowField

def test_config_basic_metadata_inclusion():
    """Verify that encoder, decoder, and mm_field are stored in the returned metadata."""
    def dummy_encoder(x): return x
    def dummy_decoder(x): return x
    class DummyField(MarshmallowField): pass

    metadata = config(
        encoder=dummy_encoder,
        decoder=dummy_decoder,
        mm_field=DummyField()
    )
    assert metadata["dataclasses_json"]["encoder"] is dummy_encoder
    assert metadata["dataclasses_json"]["decoder"] is dummy_decoder
    assert isinstance(metadata["dataclasses_json"]["mm_field"], DummyField)

def test_config_field_name_override_with_letter_case():
    """When field_name is provided, the letter_case function should be overridden to return that name."""
    def custom_case(name: str) -> str:
        return name.upper()

    metadata = config(
        letter_case=custom_case,
        field_name="custom_field"
    )
    # The stored letter_case should be a wrapper that ignores its input
    letter_case_func = metadata["dataclasses_json"]["letter_case"]
    assert letter_case_func("ignored") == "custom_field"
    # Ensure that the original custom_case is not called
    assert letter_case_func.__name__ == "override"

def test_config_invalid_undefined_raises_error():
    """Providing an invalid undefined string should raise UndefinedParameterError."""
    with pytest.raises(UndefinedParameterError) as excinfo:
        config(undefined="invalid_action")
    assert "must be one of" in str(excinfo.value)
