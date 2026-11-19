import pytest
from mimesis.providers.base import ProviderRegistry


class DummyProvider:
    """Simple dummy provider class for testing registration."""
    pass


def test_register_and_get_single_provider():
    # Ensure registry starts empty
    assert ProviderRegistry.get_all() == {}

    # Register a dummy provider
    ProviderRegistry.register("dummy", DummyProvider)

    # Verify that the provider is retrievable by name
    retrieved = ProviderRegistry.get("dummy")
    assert retrieved is DummyProvider

    # Verify that get_all now contains the provider
    all_providers = ProviderRegistry.get_all()
    assert "dummy" in all_providers
    assert all_providers["dummy"] is DummyProvider


def test_get_returns_none_for_unregistered_name():
    # Ensure that querying a non-existent provider returns None
    assert ProviderRegistry.get("nonexistent") is None


def test_register_overwrites_existing_provider():
    class FirstProvider:
        pass

    class SecondProvider:
        pass

    # Register first provider
    ProviderRegistry.register("dup", FirstProvider)
    assert ProviderRegistry.get("dup") is FirstProvider

    # Register second provider with same name, should overwrite
    ProviderRegistry.register("dup", SecondProvider)
    assert ProviderRegistry.get("dup") is SecondProvider

    # Ensure get_all reflects the latest registration
    all_providers = ProviderRegistry.get_all()
    assert all_providers["dup"] is SecondProvider
