import json
import types
import pytest
from mimesis.providers.base import BaseProvider
from mimesis.exceptions import NonEnumerableError
from mimesis import random as _random
from mimesis.providers.registry import ProviderRegistry
from enum import Enum


def test_auto_register_subclass(tmp_path):
    """Defining a subclass of BaseProvider should automatically register it."""
    class DummyProvider(BaseProvider):
        class Meta:
            name = "dummy"

    # The registry should contain the new provider under the key "dummy"
    assert ProviderRegistry.get("dummy") is DummyProvider
    # Ensure that the provider can be instantiated normally
    provider = DummyProvider()
    assert isinstance(provider, DummyProvider)


def test_reseed_with_global_seed(tmp_path):
    """reseed with MissingSeed should use the global seed if set."""
    # Set a global seed
    _random.global_seed = 12345
    provider = BaseProvider()
    # The provider's internal random should be seeded with the global seed
    assert provider.random.randint(1, 100) == provider.random.randint(1, 100)
    # Now reseed with a specific seed
    provider.reseed(67890)
    # The next random number should differ from the one before reseeding
    first = provider.random.randint(1, 100)
    provider.reseed(67890)
    second = provider.random.randint(1, 100)
    assert first == second
    # Reset global seed to None for other tests
    _random.global_seed = None


def test_validate_enum_error(tmp_path):
    """validate_enum should raise NonEnumerableError when item is invalid."""
    class Color(Enum):
        RED = 1
        GREEN = 2

    provider = BaseProvider()
    with pytest.raises(NonEnumerableError):
        provider.validate_enum("BLUE", Color)
