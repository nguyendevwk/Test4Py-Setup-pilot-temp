import json
import os
import tempfile
import types
import pytest
from enum import Enum

from mimesis.providers.base import BaseProvider, NonEnumerableError
from mimesis.random import Random
from mimesis.constants import DATADIR

# Helper enum for testing validate_enum
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# 1. Test automatic provider registration via __init_subclass__
def test_auto_register_provider(tmp_path):
    # Define a dummy provider subclass
    class DummyProvider(BaseProvider):
        class Meta:
            name = "dummy"
            auto_register = True

    # The registry should contain the provider after definition
    from mimesis.providers.registry import ProviderRegistry
    assert ProviderRegistry.get("dummy") is DummyProvider

    # Disable auto_register and ensure it is not registered
    class NoRegisterProvider(BaseProvider):
        class Meta:
            name = "no_register"
            auto_register = False

    assert ProviderRegistry.get("no_register") is None

# 2. Test seed handling and reseeding behavior
def test_seed_and_reseed():
    # Create two providers with the same explicit seed
    provider_a = BaseProvider(seed=12345)
    provider_b = BaseProvider(seed=12345)

    # They should produce the same random number
    assert provider_a.random.randint(1, 100) == provider_b.random.randint(1, 100)

    # Reseed provider_a with a different seed
    provider_a.reseed(54321)
    assert provider_a.random.randint(1, 100) != provider_b.random.randint(1, 100)

    # Reseed with MissingSeed (default) should use global seed if set
    provider_c = BaseProvider()
    provider_c.reseed()
    # Ensure that reseeding with MissingSeed does not raise
    assert provider_c._has_seed() is True

# 3. Test validate_enum and error handling
def test_validate_enum_and_file_reading(tmp_path):
    provider = BaseProvider()

    # Valid enum item
    assert provider.validate_enum(Color.RED, Color) == 1

    # None should pick a random enum item
    result = provider.validate_enum(None, Color)
    assert result in (1, 2, 3)

    # Invalid item should raise NonEnumerableError
    with pytest.raises(NonEnumerableError):
        provider.validate_enum("not_an_enum", Color)

    # Test _read_global_file raises FileNotFoundError for missing file
    missing_file = "nonexistent.json"
    with pytest.raises(FileNotFoundError):
        provider._read_global_file(missing_file)

    # Create a temporary JSON file in the expected global directory
    global_dir = DATADIR / "global"
    global_dir.mkdir(parents=True, exist_ok=True)
    test_file = global_dir / "test.json"
    test_data = {"key": "value"}
    test_file.write_text(json.dumps(test_data))

    # Reading the file should return the JSON data
    assert provider._read_global_file("test.json") == test_data
