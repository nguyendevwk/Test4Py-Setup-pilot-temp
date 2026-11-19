import pytest
from dataclasses_json.cfg import config
from dataclasses_json.undefined import Undefined, UndefinedParameterError
from marshmallow.fields import Field as MarshmallowField
from dataclasses_json.stringcase import camelcase


def test_config_with_all_options():
    """Verify that all supported options are correctly stored in the metadata."""
    def dummy_encoder(x): return x
    def dummy_decoder(x): return x
    class DummyField(MarshmallowField):
        pass

    metadata = config(
        encoder=dummy_encoder,
        decoder=dummy_decoder,
        mm_field=DummyField(),
        letter_case=camelcase,
        undefined="ignore",
        field_name="custom_name",
        exclude=lambda x: False,
    )
    lib_meta = metadata["dataclasses_json"]
    assert lib_meta["encoder"] is dummy_encoder
    assert lib_meta["decoder"] is dummy_decoder
    assert isinstance(lib_meta["mm_field"], DummyField)
    # letter_case should be overridden to return the custom field name
    assert lib_meta["letter_case"]("ignored") == "custom_name"
    assert lib_meta["undefined"] is Undefined.IGNORE
    assert lib_meta["exclude"] is not None
    assert lib_meta["exclude"]("anything") is False


def test_config_with_minimal_and_field_name_override():
    """When only field_name is provided, letter_case should default to identity."""
    metadata = config(field_name="my_field")
    lib_meta = metadata["dataclasses_json"]
    # letter_case should be a function that returns the field name unchanged
    assert lib_meta["letter_case"]("ignored") == "my_field"
    # No other keys should be present
    assert set(lib_meta.keys()) == {"letter_case"}


def test_config_invalid_undefined_raises():
    """Providing an invalid undefined string should raise UndefinedParameterError."""
    with pytest.raises(UndefinedParameterError) as excinfo:
        config(undefined="nonexistent_action")
    assert "must be one of" in str(excinfo.value)
