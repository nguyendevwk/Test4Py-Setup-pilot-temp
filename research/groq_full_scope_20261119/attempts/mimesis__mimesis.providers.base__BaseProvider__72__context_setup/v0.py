import json
import os
import types
import pytest
from mimesis.providers.base import BaseProvider, ProviderRegistry
from mimesis.exceptions import NonEnumerableError
from mimesis.types import MissingSeed
from mimesis import random as _random


class DummyEnum:
    """Simple enum-like class for testing validate_enum."""
    class Item:
        def __init__(self, value):
            self.value = value

    ONE = Item(1)
    TWO = Item(2)


def test_reseed_default_behavior():
    """When seed is MissingSeed, reseed uses global seed and produces deterministic output."""
    # Set a global seed
    _random.global_seed = 12345
    provider = BaseProvider()
    first_value = provider.random.randint(0, 100)
    # Reseed with MissingSeed again
    provider.reseed()
    second_value = provider.random.randint(0, 100)
    # With same global seed, values should match
    assert first_value == second_value
    # Ensure that reseed with a concrete seed changes the generator
    provider.reseed(999)
    third_value = provider.random.randint(0, 100)
    assert third_value != first_value


def test_validate_enum_error_and_success():
    """validate_enum should return value for valid enum and raise for invalid."""
    provider = BaseProvider()
    # Valid enum instance
    assert provider.validate_enum(DummyEnum.ONE, DummyEnum) == 1
    # None should pick a random enum item
    result = provider.validate_enum(None, DummyEnum)
    assert result in (1, 2)
    # Invalid type should raise NonEnumerableError
    with pytest.raises(NonEnumerableError):
        provider.validate_enum("invalid", DummyEnum)


def test_provider_registry_auto_registration():
    """Subclassing BaseProvider with Meta.name should auto-register in ProviderRegistry."""
    class TestProvider(BaseProvider):
        class Meta:
            name = "test_provider"
            auto_register = True

    # The registry should contain the new provider
    registry = ProviderRegistry.get_all()
    assert "test_provider" in registry
    assert registry["test_provider"] is TestProvider
    # Retrieving by name should return the same class
    assert ProviderRegistry.get("test_provider") is TestProvider
