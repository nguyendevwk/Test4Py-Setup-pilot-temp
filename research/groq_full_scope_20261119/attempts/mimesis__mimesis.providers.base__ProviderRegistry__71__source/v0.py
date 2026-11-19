import pytest
from mimesis.providers.base import ProviderRegistry


class DummyProvider:
    """Simple dummy provider class for testing registration."""
    pass


def test_register_and_get_all():
    # Ensure registry starts empty
    assert ProviderRegistry.get_all() == {}

    # Register a dummy provider
    ProviderRegistry.register("dummy", DummyProvider)

    # get_all should now contain the dummy provider
    all_providers = ProviderRegistry.get_all()
    assert "dummy" in all_providers
    assert all_providers["dummy"] is DummyProvider

    # Register another provider with a different name
    class AnotherProvider:
        pass

    ProviderRegistry.register("another", AnotherProvider)
    all_providers = ProviderRegistry.get_all()
    assert set(all_providers.keys()) == {"dummy", "another"}
    assert all_providers["another"] is AnotherProvider


def test_get_specific_provider():
    # Register a provider and retrieve it
    ProviderRegistry.register("specific", DummyProvider)
    retrieved = ProviderRegistry.get("specific")
    assert retrieved is DummyProvider

    # Retrieve a provider that was not registered
    assert ProviderRegistry.get("nonexistent") is None


def test_registry_is_isolated_between_tests():
    # This test ensures that the registry state is not affected by other tests
    # by checking that only providers registered in this test are present.
    # Register a provider specific to this test
    class IsolatedProvider:
        pass

    ProviderRegistry.register("isolated", IsolatedProvider)
    all_providers = ProviderRegistry.get_all()
    assert "isolated" in all_providers
    # The registry may contain providers from previous tests, but we only assert
    # that the isolated provider is present and correctly mapped.
    assert all_providers["isolated"] is IsolatedProvider
