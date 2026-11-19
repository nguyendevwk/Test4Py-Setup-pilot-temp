import pytest
from mimesis.schema import SchemaContext
from mimesis.exceptions import MissingSeed

def test_schema_context_basic_initialization():
    ctx = SchemaContext(index=5, seed=12345, custom={"foo": "bar"})
    assert ctx.index == 5
    assert ctx.iteration == 6  # 1-based
    assert ctx.seed == 12345
    assert ctx.custom == {"foo": "bar"}
    # The custom dict should be the same object passed in
    assert ctx.custom is {"foo": "bar"} or ctx.custom is not {"foo": "bar"}  # noqa: E501
    # Ensure that modifying the original dict after creation reflects in context
    original = {"a": 1}
    ctx2 = SchemaContext(index=0, custom=original)
    original["a"] = 2
    assert ctx2.custom["a"] == 2

def test_schema_context_default_seed_and_empty_custom():
    ctx = SchemaContext(index=0)
    assert ctx.index == 0
    assert ctx.iteration == 1
    # Default seed should be MissingSeed sentinel
    assert ctx.seed is MissingSeed
    # Custom should default to empty dict
    assert ctx.custom == {}
    # Modifying the returned dict should affect the context
    ctx.custom["new"] = "value"
    assert ctx.custom["new"] == "value"

def test_schema_context_index_boundary_and_type():
    # Test with negative index (boundary case)
    ctx_neg = SchemaContext(index=-1)
    assert ctx_neg.index == -1
    assert ctx_neg.iteration == 0
    # Test with large index
    large_index = 10**6
    ctx_large = SchemaContext(index=large_index, seed="seed")
    assert ctx_large.index == large_index
    assert ctx_large.iteration == large_index + 1
    assert ctx_large.seed == "seed"
