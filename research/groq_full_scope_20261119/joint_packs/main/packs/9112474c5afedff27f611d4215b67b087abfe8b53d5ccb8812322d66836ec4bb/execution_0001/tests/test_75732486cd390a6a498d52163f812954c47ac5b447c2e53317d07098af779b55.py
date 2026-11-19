import pytest
from mimesis.providers.base import ProviderRegistry

class DummyProvider:
    """Simple dummy provider class for testing."""
    pass

def test_register_and_get():
    # Register a dummy provider and verify it can be retrieved
    ProviderRegistry.register("dummy", DummyProvider)
    retrieved = ProviderRegistry.get("dummy")
    assert retrieved is DummyProvider, "Registered provider should be returned by get()"

def test_get_all_returns_copy():
    # Ensure get_all returns a copy and modifications do not affect the registry
    ProviderRegistry.register("copy_test", DummyProvider)
    all_providers = ProviderRegistry.get_all()
    assert "copy_test" in all_providers
    assert all_providers["copy_test"] is DummyProvider
    # Modify the returned dict
    all_providers.pop("copy_test")
    # Original registry should still contain the provider
    assert ProviderRegistry.get("copy_test") is DummyProvider

def test_get_nonexistent_returns_none():
    # Requesting a provider that hasn't been registered should return None
    assert ProviderRegistry.get("nonexistent") is None
