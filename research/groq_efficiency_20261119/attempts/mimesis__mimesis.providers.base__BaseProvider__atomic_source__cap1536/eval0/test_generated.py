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
    # After reseeding, the next random number should be deterministic
    second = provider.random.randint(1, 100)
    provider.reseed(seed=12345)
    third = provider.random.randint(1, 100)
    assert second == third
    assert first != second  # unlikely but ensures reseed had effect

# --------------------------------------------------------------------------- #
# Test 3: validate_enum raises NonEnumerableError for invalid input
# --------------------------------------------------------------------------- #
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

def test_validate_enum_error():
    provider = DummyProvider()
    with pytest.raises(NonEnumerableError):
        provider.validate_enum(item="not_an_enum", enum=Color)
