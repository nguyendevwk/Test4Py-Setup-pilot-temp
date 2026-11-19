import json
import os
import pytest
from mimesis.providers.base import BaseProvider, ProviderRegistry
from mimesis.exceptions import NonEnumerableError
from mimesis.random import Random
from mimesis.types import MissingSeed


def test_custom_random_initialization(tmp_path):
    """BaseProvider should accept a custom Random instance and use it."""
    # Create a custom Random instance with a fixed seed
    custom_random = Random(seed=123)
    provider = BaseProvider(random=custom_random)
    # The provider's random should be the same instance
    assert provider.random is custom_random
    # The provider should produce deterministic values
    first = provider.random.randint(1, 10)
    provider.reseed(123)
    second = provider.random.randint(1, 10)
    assert first == second, "Re-seeding with the same seed should produce the same sequence"


def test_validate_enum_raises_nonenumerable_error():
    """validate_enum should raise NonEnumerableError when item is invalid."""
    provider = BaseProvider()
    # Define a simple enum-like class for testing
    class DummyEnum:
        class Item:
            value = "valid"

    # Passing None should choose a random enum item (no error)
    result = provider.validate_enum(None, DummyEnum)
    assert result == "valid"

    # Passing an instance of the enum should return its value
    instance = DummyEnum.Item()
    result = provider.validate_enum(instance, DummyEnum)
    assert result == "valid"

    # Passing an invalid type should raise NonEnumerableError
    with pytest.raises(NonEnumerableError):
        provider.validate_enum("invalid", DummyEnum)


def test_read_global_file_not_found(tmp_path):
    """_read_global_file should raise FileNotFoundError for missing files."""
    provider = BaseProvider()
    # Use a filename that is highly unlikely to exist
    missing_file = "this_file_does_not_exist.json"
    with pytest.raises(FileNotFoundError):
        provider._read_global_file(missing_file)


def test_provider_registry_auto_registration():
    """Subclassing BaseProvider should auto-register the provider."""
    # Ensure the registry is empty before the test
    ProviderRegistry._providers.clear()

    class TestProvider(BaseProvider):
        class Meta:
            name = "test_provider"

    # After definition, the provider should be registered
    registered = ProviderRegistry.get("test_provider")
    assert registered is TestProvider, "Provider should be auto-registered with its Meta.name"

    # The registry should contain exactly one provider
    all_providers = ProviderRegistry.get_all()
    assert len(all_providers) == 1
    assert "test_provider" in all_providers
