import json
import os
import tempfile
import types
import pytest
from mimesis.providers.base import BaseProvider
from mimesis.exceptions import NonEnumerableError
from mimesis.types import Seed, MissingSeed
from enum import Enum

# --------------------------------------------------------------------------- #
# Test 1: __str__ returns the class name
# --------------------------------------------------------------------------- #
class DummyProvider(BaseProvider):
    class Meta:
        name = "dummy"

def test_str_representation():
    provider = DummyProvider()
    assert str(provider) == "DummyProvider"

# --------------------------------------------------------------------------- #
# Test 2: reseed changes the internal random generator state
# --------------------------------------------------------------------------- #
def test_reseed_changes_state():
    provider = DummyProvider()
    # Capture a random number before reseeding
    first = provider.random.randint(1, 100)
    # Reseed with a fixed seed
    provider.reseed(seed=12345)
    # After reseeding, the sequence should start from the same seed
    second = provider.random.randint(1, 100)
    provider.reseed(seed=12345)
    third = provider.random.randint(1, 100)
    # The two numbers after reseeding with the same seed must be equal
    assert second == third
    # The number before reseeding should differ
    assert first != second

# --------------------------------------------------------------------------- #
# Test 3: validate_enum raises NonEnumerableError for invalid input
# --------------------------------------------------------------------------- #
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

def test_validate_enum_invalid_input():
    provider = DummyProvider()
    with pytest.raises(NonEnumerableError):
        provider.validate_enum("not_an_enum", Color)
