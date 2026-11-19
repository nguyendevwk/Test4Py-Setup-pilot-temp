import pytest
from dataclasses_json.cfg import config
from dataclasses_json.undefined import Undefined, UndefinedParameterError
from marshmallow.fields import Integer

def test_config_basic_metadata_and_options():
    # Basic usage: provide metadata and all optional arguments
    def custom_encoder(x): return str(x)
    def custom_decoder(x): return int(x)
    def exclude_func(x): return False

    metadata = {"existing": "value"}
    result = config(
        metadata=metadata,
        encoder=custom_encoder,
        decoder=custom_decoder,
        mm_field=Integer(),
        letter_case=lambda s: s.upper(),
        undefined=Undefined.REJECT,
        field_name="custom_name",
        exclude=exclude_func,
    )

    # The original metadata dict should be updated in place
    assert metadata is result
    lib_meta = metadata["dataclasses_json"]
    assert lib_meta["encoder"] is custom_encoder
    assert lib_meta["decoder"] is custom_decoder
    assert lib_meta["mm_field"] is Integer()
    assert lib_meta["letter_case"]("test") == "TEST"
    assert lib_meta["undefined"] is Undefined.REJECT
    assert lib_meta["exclude"] is exclude_func
    # field_name overrides letter_case
    assert lib_meta["letter_case"]("ignored") == "custom_name"

def test_config_field_name_override_without_letter_case():
    # When field_name is provided without letter_case, it should be used directly
    metadata = {}
    result = config(metadata=metadata, field_name="explicit_name")
    lib_meta = result["dataclasses_json"]
    # letter_case should be a function that returns the field_name
    assert lib_meta["letter_case"]("any") == "explicit_name"

def test_config_invalid_undefined_raises_error():
    # Passing an invalid string for undefined should raise UndefinedParameterError
    metadata = {}
    with pytest.raises(UndefinedParameterError) as excinfo:
        config(metadata=metadata, undefined="invalid_action")
    assert "must be one of" in str(excinfo.value)
