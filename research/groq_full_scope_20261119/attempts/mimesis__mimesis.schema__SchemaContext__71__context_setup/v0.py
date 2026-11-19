import pytest
from mimesis.schema import SchemaContext

def test_schema_context_basic_initialization():
    """Verify that a SchemaContext correctly stores index, iteration, seed and custom data."""
    ctx = SchemaContext(index=5, seed=42, custom={"foo": "bar"})
    assert ctx.index == 5
    assert ctx.iteration == 6  # iteration is 1-based
    assert ctx.seed == 42
    assert ctx.custom == {"foo": "bar"}

def test_schema_context_default_custom_and_seed():
    """Ensure that default values for custom and seed are handled correctly."""
    ctx = SchemaContext(index=0)
    assert ctx.index == 0
    assert ctx.iteration == 1
    assert ctx.seed is None  # MissingSeed is represented as None
    assert ctx.custom == {}  # default to empty dict

def test_schema_context_invalid_index_type():
    """Passing a non-integer index should raise a TypeError."""
    with pytest.raises(TypeError):
        SchemaContext(index="not-an-int")  # type: ignore[arg-type]
