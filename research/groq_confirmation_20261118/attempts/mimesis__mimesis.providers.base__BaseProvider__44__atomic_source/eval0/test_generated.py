import json
import os
import tempfile
import types
import pytest
from mimesis.providers.base import BaseProvider
from mimesis.exceptions import NonEnumerableError
from mimesis import random as _random
from mimesis.providers.registry import ProviderRegistry

# --------------------------------------------------------------------------- #
# Test 1: Automatic registration of a provider subclass
# --------------------------------------------------------------------------- #
def test_auto_register_subclass(tmp_path):
    # Define a dummy provider subclass with Meta.name
    class DummyProvider(BaseProvider):
        class Meta:
            name = "dummy"

    # The provider should be registered automatically
    assert ProviderRegistry.get("dummy") is DummyProvider

    # Ensure that the registry contains the provider
    registry_keys = list(ProviderRegistry._registry.keys())
    assert "dummy" in registry_keys
    assert ProviderRegistry._registry["dummy"] is DummyProvider

# --------------------------------------------------------------------------- #
# Test 2: Reseed behavior with explicit and default seeds
# --------------------------------------------------------------------------- #
def test_reseed_behavior():
    # Create two providers with the same explicit seed
    provider_a = BaseProvider(seed=123)
    provider_b = BaseProvider(seed=123)

    # They should produce the same random number sequence
    assert provider_a.random.randint(1, 100) == provider_b.random.randint(1, 100)

    # Now reseed provider_a with a different seed
    provider_a.reseed(456)
    assert provider_a.random.randint(1, 100) != provider_b.random.randint(1, 100)

    # Reseed with MissingSeed should use global seed
    global_seed = _random.global_seed
    provider_c = BaseProvider()
    provider_c.reseed()
    assert provider_c.random.randint(1, 100) == provider_a.random.randint(1, 100)

# --------------------------------------------------------------------------- #
# Test 3: validate_enum raises NonEnumerableError for invalid input
# --------------------------------------------------------------------------- #
def test_validate_enum_error():
    class DummyEnum:
        class Item:
            value = "value"

    provider = BaseProvider()

    # Passing None should choose a random enum item (no error)
    result = provider.validate_enum(None, DummyEnum)
    assert result == "value"

    # Passing a valid enum instance should return its value
    enum_instance = DummyEnum.Item()
    result = provider.validate_enum(enum_instance, DummyEnum)
    assert result == "value"

    # Passing an invalid type should raise NonEnumerableError
    with pytest.raises(NonEnumerableError):
        provider.validate_enum("invalid", DummyEnum)
