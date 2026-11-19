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

    def generate(self):
        self.called = True
        return "dummy_value"


def test_generic_attribute_access_and_lazy_initialization():
    """Generic should lazily instantiate providers on first attribute access."""
    g = Generic(locale=Locale.EN)
    # Initially, no provider attributes are present
    assert not hasattr(g, "dummy")
    # Accessing a non-existent provider should raise AttributeError
    with pytest.raises(AttributeError):
        _ = g.nonexistent

    # Add DummyProvider via add_provider
    g.add_provider(DummyProvider)
    # Provider is now available as attribute
    assert hasattr(g, "dummy")
    provider = g.dummy
    assert isinstance(provider, DummyProvider)
    # Calling a method on the provider should work
    assert provider.generate() == "dummy_value"
    assert provider.called is True


def test_generic_reseed_propagates_to_providers():
    """Reseeding Generic should propagate to all providers that support reseed."""
    g = Generic(seed=123)
    # Add DummyProvider which inherits BaseProvider and thus has reseed
    g.add_provider(DummyProvider)
    provider = g.dummy
    # Ensure provider's seed is initially set
    assert provider.seed == 123

    # Reseed Generic with a new seed
    g.reseed(456)
    # Provider's seed should now be updated
    assert provider.seed == 456


def test_generic_add_provider_errors():
    """add_provider should raise TypeError for invalid inputs."""
    g = Generic()
    # Passing a non-class should raise TypeError
    with pytest.raises(TypeError, match="must be a class"):
        g.add_provider(42)

    # Passing a class that is not a subclass of BaseProvider should raise TypeError
    class NotAProvider:
        pass

    with pytest.raises(TypeError, match="must be a subclass"):
        g.add_provider(NotAProvider)

    # Adding Generic itself should raise TypeError
    with pytest.raises(TypeError, match="Cannot add Generic instance"):
        g.add_provider(Generic)
