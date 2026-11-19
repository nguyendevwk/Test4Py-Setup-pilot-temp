import pytest
from mimesis.schema import SchemaContext


def test_schema_context_basic_initialization(tmp_path):
    """Verify that the context correctly stores index, iteration, seed and custom data."""
    seed_value = 12345
    custom_data = {"foo": "bar"}
    ctx = SchemaContext(index=5, seed=seed_value, custom=custom_data)

    # Basic attributes
    assert ctx.index == 5
    assert ctx.iteration == 6  # iteration is 1-based
    assert ctx.seed == seed_value
    assert ctx.custom is custom_data  # same reference
    assert ctx.custom["foo"] == "bar"

    # Mutating the context's custom dict should reflect in the original dict
    ctx.custom["baz"] = "qux"
    assert custom_data["baz"] == "qux"


def test_schema_context_default_custom_and_seed(tmp_path):
    """Check that default values are used when optional arguments are omitted."""
    ctx = SchemaContext(index=0)

    # Default seed should be MissingSeed sentinel (not None)
    from mimesis.types import MissingSeed
    assert ctx.seed is MissingSeed

    # Default custom should be an empty dict
    assert isinstance(ctx.custom, dict)
    assert ctx.custom == {}

    # Index and iteration
    assert ctx.index == 0
    assert ctx.iteration == 1


def test_schema_context_index_boundary_and_type(tmp_path):
    """Ensure that index can be zero and that non-integer indices are accepted (no runtime check)."""
    # Zero index
    ctx_zero = SchemaContext(index=0)
    assert ctx_zero.index == 0
    assert ctx_zero.iteration == 1

    # Negative index (boundary test)
    ctx_negative = SchemaContext(index=-1)
    assert ctx_negative.index == -1
    assert ctx_negative.iteration == 0

    # Non-integer index (e.g., float) – no type enforcement in __init__
    ctx_float = SchemaContext(index=3.14)
    assert ctx_float.index == 3.14
    assert ctx_float.iteration == 4.14
