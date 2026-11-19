import pytest
from mimesis.providers.base import ProviderRegistry


class DummyProvider:
    """Simple dummy provider class for testing registration."""
    pass


def test_register_and_get_single_provider():
    # Register a dummy provider and verify it can be retrieved.
    ProviderRegistry.register("dummy", DummyProvider)
    retrieved = ProviderRegistry.get("dummy")
    assert retrieved is DummyProvider, "ProviderRegistry should return the registered class"


def test_get_all_returns_copy_and_is_independent():
    # Register two providers and check that get_all returns a copy.
    ProviderRegistry.register("first", DummyProvider)
    ProviderRegistry.register("second", DummyProvider)
    all_providers = ProviderRegistry.get_all()
    assert isinstance(all_providers, dict), "get_all should return a dictionary"
    assert set(all_providers.keys()) == {"dummy", "first", "second"}, "All registered names should be present"
    # Modify the returned dict and ensure the registry is unchanged.
    all_providers.pop("dummy")
    assert ProviderRegistry.get("dummy") is DummyProvider, "Registry should not be affected by external modifications"


def test_get_returns_none_for_unregistered_name():
    # Ensure that querying an unknown provider returns None.
    assert ProviderRegistry.get("nonexistent") is None, "Unregistered provider names should return None"
