import pytest
from mimesis.providers.generic import Generic
from mimesis.providers.base import BaseProvider, ProviderRegistry
from mimesis.types import MissingSeed


class DummyProvider(BaseProvider):
    """Simple provider that records reseed calls."""

    def __init__(self, seed=MissingSeed):
        super().__init__(seed=seed)
        self.reseed_calls = []

    def reseed(self, seed=MissingSeed):
        super().reseed(seed)
        self.reseed_calls.append(seed)


def test_generic_provider_access_and_str():
    """Generic should expose providers as attributes and have a readable string."""
    g = Generic()
    # The 'address' provider is a common BaseProvider; it should be available.
    assert hasattr(g, "address")
    # Accessing the provider should return an instance of the provider class.
    address_provider = getattr(g, "address")
    assert isinstance(address_provider, BaseProvider)
    # The string representation should include the locale.
    assert str(g).startswith("Generic <")
    assert str(g).endswith(">")  # simple format check


def test_add_provider_invalid_and_valid():
    """add_provider should reject non‑subclass and accept a valid provider."""
    g = Generic()
    # Reject a non‑class argument.
    with pytest.raises(TypeError, match="must be a class"):
        g.add_provider(42)

    # Reject a class that is not a BaseProvider subclass.
    class NotProvider:
        pass

    with pytest.raises(TypeError, match="must be a subclass"):
        g.add_provider(NotProvider)

    # Valid provider should be added and accessible.
    g.add_provider(DummyProvider)
    assert hasattr(g, "dummyprovider")
    assert isinstance(g.dummyprovider, DummyProvider)

    # Using the in‑place addition operator should also work.
    g += DummyProvider
    assert hasattr(g, "dummyprovider")
    assert isinstance(g.dummyprovider, DummyProvider)


def test_reseed_propagates_to_providers(tmp_path):
    """reseed should propagate to all providers that implement reseed."""
    g = Generic()
    # Add a dummy provider that records reseed calls.
    g.add_provider(DummyProvider)
    dummy = g.dummyprovider
    assert dummy.reseed_calls == []

    # Reseed Generic with a specific seed.
    g.reseed(seed=12345)
    # The dummy provider should have recorded the reseed call.
    assert dummy.reseed_calls == [12345]

    # Reseed again with a different seed.
    g.reseed(seed=67890)
    assert dummy.reseed_calls == [12345, 67890]
