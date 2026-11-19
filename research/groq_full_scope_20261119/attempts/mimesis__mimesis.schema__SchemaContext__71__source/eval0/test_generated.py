import pytest
from mimesis.schema import SchemaContext
from mimesis.types import MissingSeed


def test_schema_context_initialization_defaults():
    """SchemaContext should correctly set index, iteration, seed and custom defaults."""
    ctx = SchemaContext(index=5)
    assert ctx.index == 5
    assert ctx.iteration == 6  # iteration is 1-based
    assert ctx.seed is MissingSeed
    assert ctx.custom == {}


def test_schema_context_with_custom_and_seed():
    """Providing custom data and a seed should store them unchanged."""
    custom_data = {"foo": "bar", "num": 42}
    seed_value = 12345
    ctx = SchemaContext(index=0, seed=seed_value, custom=custom_data)
    assert ctx.index == 0
    assert ctx.iteration == 1
    assert ctx.seed == seed_value
    assert ctx.custom is custom_data
    # Mutating the returned custom dict should not affect the original
    ctx.custom["new"] = "value"
    assert "new" in ctx.custom
    assert "new" not in custom_data


def test_schema_context_index_and_iteration_consistency():
    """Index and iteration should remain consistent across multiple instances."""
    indices = [0, 1, 10, 999]
    contexts = [SchemaContext(i) for i in indices]
    for i, ctx in zip(indices, contexts):
        assert ctx.index == i
        assert ctx.iteration == i + 1
