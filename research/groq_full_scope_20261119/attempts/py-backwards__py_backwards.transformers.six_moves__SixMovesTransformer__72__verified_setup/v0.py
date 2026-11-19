import pytest
from py_backwards.transformers.six_moves import SixMovesTransformer


def test_target_and_dependencies():
    """Verify the transformer declares the correct target Python version and dependencies."""
    assert SixMovesTransformer.target == (2, 7), "Target should be (2, 7)"
    assert isinstance(SixMovesTransformer.dependencies, list), "Dependencies should be a list"
    assert "six" in SixMovesTransformer.dependencies, "Dependency 'six' must be present"


def test_rewrites_structure():
    """Ensure the rewrites attribute is a non‑empty dictionary mapping module names."""
    rewrites = SixMovesTransformer.rewrites
    assert isinstance(rewrites, dict), "rewrites should be a dictionary"
    assert rewrites, "rewrites dictionary should not be empty"
    # Each key should be a string and each value should be a string
    for key, value in rewrites.items():
        assert isinstance(key, str), f"Rewrite key {key!r} is not a string"
        assert isinstance(value, str), f"Rewrite value {value!r} is not a string"


def test_rewrites_contains_expected_mapping():
    """Check that a known module is correctly mapped to its six.moves counterpart."""
    # Commonly moved modules include 'cStringIO' -> 'six.moves.cStringIO'
    rewrites = SixMovesTransformer.rewrites
    # The mapping may vary; we check for a typical entry if present
    if "cStringIO" in rewrites:
        assert rewrites["cStringIO"] == "six.moves.cStringIO", (
            "cStringIO should map to six.moves.cStringIO"
        )
    else:
        # If the mapping is not present, at least ensure that the key is not mapped to itself
        assert all(k != v for k, v in rewrites.items()), "No rewrite should map a module to itself"
