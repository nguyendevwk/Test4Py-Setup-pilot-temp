import pytest
from dataclasses_json.cfg import config, LetterCase
from dataclasses_json.undefined import Undefined, UndefinedParameterError
from marshmallow.fields import Field as MarshmallowField

def test_config_with_encoder_decoder_and_mm_field():
    def enc(x): return str(x)
    def dec(x): return int(x)
    class DummyField(MarshmallowField):
        pass
    metadata = {"existing": "value"}
    result = config(
        metadata=metadata,
        encoder=enc,
        decoder=dec,
        mm_field=DummyField(),
        letter_case=LetterCase.SNAKE,
        undefined=Undefined.IGNORE,
        field_name="custom_name",
        exclude=lambda x: False,
    )
    # Ensure original metadata dict is returned and enriched correctly
    assert result is metadata
    lib_meta = metadata["dataclasses_json"]
    assert lib_meta["encoder"] is enc
    assert lib_meta["decoder"] is dec
    assert lib_meta["mm_field"] is DummyField
    assert lib_meta["letter_case"] is LetterCase.SNAKE
    assert lib_meta["undefined"] is Undefined.IGNORE
    assert lib_meta["exclude"] is not None
    # field_name override should change letter_case behavior
    assert lib_meta["letter_case"]("ignored") == "custom_name"

def test_config_field_name_override_without_letter_case():
    metadata = {}
    result = config(
        metadata=metadata,
        field_name="fixed_name",
    )
    lib_meta = metadata["dataclasses_json"]
    # letter_case should be a function that returns the field_name
    assert lib_meta["letter_case"]("any") == "fixed_name"
    # No other keys should be present
    assert set(lib_meta.keys()) == {"letter_case"}

def test_config_invalid_undefined_raises():
    metadata = {}
    with pytest.raises(UndefinedParameterError) as excinfo:
        config(metadata=metadata, undefined="nonexistent_action")
    assert "must be one of" in str(excinfo.value)
