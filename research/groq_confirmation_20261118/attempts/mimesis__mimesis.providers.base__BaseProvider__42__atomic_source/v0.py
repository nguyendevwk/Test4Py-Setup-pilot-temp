import enum
import json
import os
import tempfile
import types
import pytest
from mimesis.providers.base import BaseProvider
from mimesis.exceptions import NonEnumerableError
from mimesis import random as _random
from mimesis.constants import DATADIR

# --------------------------------------------------------------------------- #
# 1. Test automatic registration of a subclass via __init_subclass__
# --------------------------------------------------------------------------- #
class DummyProvider(BaseProvider):
    class Meta:
        name = "dummy"

def test_auto_register_subclass(tmp_path):
    # Ensure registry is empty before test
    registry = BaseProvider.__dict__.get("ProviderRegistry", None)
    if registry is None:
        pytest.skip("ProviderRegistry not available in this environment")
    # The DummyProvider should be registered automatically
    assert "dummy" in registry._registry
    assert registry._registry["dummy"] is DummyProvider

# --------------------------------------------------------------------------- #
# 2. Test validate_enum with a valid enum and with None
# --------------------------------------------------------------------------- #
class Color(enum.Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

def test_validate_enum_valid_and_none():
    provider = BaseProvider()
    # Valid enum member
    assert provider.validate_enum(Color.RED, Color) == Color.RED.value
    # None should pick a random enum member
    # We patch the random.choice_enum_item to return a deterministic value
    original_choice = provider.random.choice_enum_item
    provider.random.choice_enum_item = lambda enum_obj: Color.GREEN
    assert provider.validate_enum(None, Color) == Color.GREEN.value
    provider.random.choice_enum_item = original_choice

# --------------------------------------------------------------------------- #
# 3. Test _has_seed behavior with different seed settings
# --------------------------------------------------------------------------- #
def test_has_seed_behavior():
    provider = BaseProvider()
    # Default: no seed set, global seed is MissingSeed
    assert not provider._has_seed()
    # Set a specific seed
    provider.reseed(12345)
    assert provider._has_seed()
    # Reset to MissingSeed
    provider.reseed(_random.MissingSeed)
    assert not provider._has_seed()
