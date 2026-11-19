import pytest
from mimesis.schema import SchemaContext


def test_schema_context_basic_initialization(tmp_path):
    """Verify that the context stores index, iteration, seed and custom correctly."""
    ctx = SchemaContext(index=5, seed=42, custom={"foo": "bar"})
    assert ctx.index == 5
    assert ctx.iteration == 6  # iteration is 1‑based
    assert ctx.seed == 42
    assert ctx.custom == {"foo": "bar"}
    # The custom dict should be the same object passed in
    ctx.custom["baz"] = "qux"
    assert ctx.custom["baz"] == "qux"


def test_schema_context_default_custom(tmp_path):
    """Ensure that a new empty dict is created when custom is not provided."""
    ctx1 = SchemaContext(index=0)
    ctx2 = SchemaContext(index=1)
    assert ctx1.custom == {}
    assert ctx2.custom == {}
    # The two custom dicts must be distinct objects
    assert ctx1.custom is not ctx2.custom
    # Mutating one should not affect the other
    ctx1.custom["a"] = 1
    assert "a" not in ctx2.custom


def test_schema_context_index_boundary_and_seed(tmp_path):
    """Test boundary values for index and seed handling."""
    # Index zero
    ctx_zero = SchemaContext(index=0, seed="seed-string")
    assert ctx_zero.index == 0
    assert ctx_zero.iteration == 1
    assert ctx_zero.seed == "seed-string"

    # Negative index
    ctx_negative = SchemaContext(index=-3, seed=3.14)
    assert ctx_negative.index == -3
    assert ctx_negative.iteration == -2
    assert ctx_negative.seed == 3.14

    # Seed as bytes
    seed_bytes = b"bytes_seed"
    ctx_bytes = SchemaContext(index=2, seed=seed_bytes)
    assert ctx_bytes.seed == seed_bytes
