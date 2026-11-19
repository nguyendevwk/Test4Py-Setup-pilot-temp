import pytest
from mimesis.providers.base import ProviderRegistry

class DummyProvider:
    """Simple dummy provider class for testing."""
    pass

def test_register_and_get():
    # Ensure registry starts empty
    assert ProviderRegistry.get_all() == {}
    # Register a dummy provider
    ProviderRegistry.register("dummy", DummyProvider)
    # Verify that the provider is retrievable
    assert ProviderRegistry.get("dummy") is DummyProvider
    # Register another provider with a different name
    ProviderRegistry.register("another", DummyProvider)
    # Verify both providers are present
    all_providers = ProviderRegistry.get_all()
    assert set(all_providers.keys()) == {"dummy", "another"}
    assert all_providers["dummy"] is DummyProvider
    assert all_providers["another"] is DummyProvider

def test_get_nonexistent_provider():
    # Attempt to get a provider that hasn't been registered
    assert ProviderRegistry.get("nonexistent") is None

def test_registry_is_copy_and_independent():
    # Register a provider
    ProviderRegistry.register("copy_test", DummyProvider)
    # Get a copy of the registry
    registry_copy = ProviderRegistry.get_all()
    # Modify the copy
    registry_copy.pop("copy_test")
    # The original registry should still contain the provider
    assert ProviderRegistry.get("copy_test") is DummyProvider
