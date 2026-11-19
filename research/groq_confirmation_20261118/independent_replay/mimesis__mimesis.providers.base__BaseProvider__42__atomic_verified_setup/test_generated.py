import json
import types
import contextlib
import pytest
from mimesis.providers.base import BaseProvider
from mimesis.exceptions import NonEnumerableError
from mimesis import random as _random
from mimesis.types import Seed, MissingSeed
from enum import Enum

# --------------------------------------------------------------------------- #
# Test 1: validate_enum correctly returns the value of a valid enum member
# --------------------------------------------------------------------------- #
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

def test_validate_enum_returns_value():
    provider = BaseProvider()
    # Passing a valid enum member should return its value
    assert provider.validate_enum(Color.RED, Color) == 1
    # Passing None should pick a random enum member
    # We cannot predict which one, but we can assert it is one of the values
    random_value = provider.validate_enum(None, Color)
    assert random_value in {c.value for c in Color}

# --------------------------------------------------------------------------- #
# Test 2: validate_enum raises NonEnumerableError for invalid input
# --------------------------------------------------------------------------- #
def test_validate_enum_raises_on_invalid():
    provider = BaseProvider()
    with pytest.raises(NonEnumerableError):
        provider.validate_enum("not_an_enum", Color)

# --------------------------------------------------------------------------- #
# Test 3: _has_seed correctly reports presence of a seed
# --------------------------------------------------------------------------- #
def test_has_seed_behavior(tmp_path):
    # Ensure global seed is None initially
    original_global = _random.global_seed
    _random.global_seed = None

    provider = BaseProvider()
    # No seed set and no global seed -> False
    assert provider._has_seed() is False

    # Set a global seed
    _random.global_seed = 12345
    assert provider._has_seed() is True

    # Reset global seed and set instance seed
    _random.global_seed = None
    provider.reseed(67890)
    assert provider._has_seed() is True

    # Reset to MissingSeed
    provider.reseed(MissingSeed)
    assert provider._has_seed() is False

    # Restore original global seed
    _random.global_seed = original_global
