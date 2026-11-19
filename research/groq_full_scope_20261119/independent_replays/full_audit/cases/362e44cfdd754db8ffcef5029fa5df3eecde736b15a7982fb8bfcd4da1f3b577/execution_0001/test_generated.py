import pytest
from mimesis.providers.base import ProviderRegistry


class DummyProvider:
    """Simple dummy provider for testing purposes."""
    pass


@pytest.fixture(autouse=True)
def reset_registry():
    """Ensure the registry is empty before each test."""
    ProviderRegistry._providers.clear()
    yield
    ProviderRegistry._providers.clear()


def test_register_and_get():
    """Register a provider and retrieve it by name."""
    ProviderRegistry.register("dummy", DummyProvider)
    retrieved = ProviderRegistry.get("dummy")
    assert retrieved is DummyProvider, "ProviderRegistry.get should return the registered class"
    assert ProviderRegistry.get("nonexistent") is None, "Unknown provider should return None"


def test_get_all_returns_copy_and_is_independent():
    """get_all should return a shallow copy that does not affect the registry."""
    ProviderRegistry.register("dummy", DummyProvider)
    all_providers = ProviderRegistry.get_all()
    assert "dummy" in all_providers
    assert all_providers["dummy"] is DummyProvider

    # Modify the returned dict and ensure the registry is unchanged
    all_providers.pop("dummy")
    assert "dummy" in ProviderRegistry.get_all(), "Registry should not be affected by modifications to the copy"


def test_registry_is_isolated_between_tests():
    """Each test should see an empty registry due to the fixture."""
    # The fixture clears the registry before this test runs
    assert ProviderRegistry.get_all() == {}, "Registry should be empty at test start"
    ProviderRegistry.register("dummy", DummyProvider)
    assert ProviderRegistry.get_all() == {"dummy": DummyProvider}
