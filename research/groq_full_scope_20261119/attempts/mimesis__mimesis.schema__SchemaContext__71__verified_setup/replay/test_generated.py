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
    """When custom is omitted, it should default to an empty dict and seed to MissingSeed."""
    ctx = SchemaContext(index=0)
    assert ctx.index == 0
    assert ctx.iteration == 1
    # MissingSeed is a sentinel object; we just check that it is not None
    assert ctx.seed is not None
    assert isinstance(ctx.custom, dict)
    assert ctx.custom == {}

def test_schema_context_invalid_index_type_raises_type_error():
    """Passing a non-integer index should raise a TypeError due to type mismatch."""
    with pytest.raises(TypeError):
        # The constructor expects an int; passing a string should trigger a TypeError
        SchemaContext(index="not-an-int")
