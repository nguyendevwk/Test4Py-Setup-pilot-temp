import pytest
from mimesis.providers.generic import Generic
from mimesis.providers.base import BaseProvider
from mimesis.locales import Locale
from mimesis.types import MissingSeed


class DummyProvider(BaseProvider):
    """Simple provider used for testing add_provider."""

    class Meta:
        name = "dummy"

    def __init__(self, seed=MissingSeed, **kwargs):
        super().__init__(seed=seed)
        self.called = False

    def value(self):
        self.called = True
        return "dummy_value"


def test_generic_attribute_access_and_lazy_initialization():
    """Generic should lazily instantiate providers on first access."""
    g = Generic(locale=Locale.EN)
    # Initially, no provider attributes exist
    assert not hasattr(g, "dummy")
    # Accessing a non-existent provider raises AttributeError
    with pytest.raises(AttributeError):
        _ = g.nonexistent
    # Add DummyProvider via add_provider
    g.add_provider(DummyProvider)
    # Provider is now available as attribute
    assert hasattr(g, "dummy")
    provider = g.dummy
    assert isinstance(provider, DummyProvider)
    # Calling provider method works
    assert provider.value() == "dummy_value"
    assert provider.called is True


def test_generic_reseed_propagates_to_providers():
    """Reseeding Generic should reseed all contained providers."""
    g = Generic(seed=123)
    g.add_provider(DummyProvider)
    provider = g.dummy
    # Ensure provider has its own seed set
    assert provider.seed == 123
    # Change seed via reseed
    g.reseed(456)
    # Provider's seed should be updated
    assert provider.seed == 456
    # Reseed again with default (MissingSeed) should keep provider's seed unchanged
    g.reseed()
    assert provider.seed == 456


def test_generic_add_provider_errors():
    """add_provider should raise TypeError for invalid inputs."""
    g = Generic()
    # Passing an instance instead of a class
    with pytest.raises(TypeError, match="must be a class"):
        g.add_provider(DummyProvider())
    # Passing a class that is not a BaseProvider subclass
    class NotProvider:
        pass
    with pytest.raises(TypeError, match="must be a subclass"):
        g.add_provider(NotProvider)
    # Passing Generic itself should raise TypeError
    with pytest.raises(TypeError, match="Cannot add Generic instance"):
        g.add_provider(Generic)
