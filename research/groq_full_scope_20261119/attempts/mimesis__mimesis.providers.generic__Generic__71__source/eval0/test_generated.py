import pytest
from mimesis.providers.generic import Generic
from mimesis.providers.base import BaseProvider
from mimesis.locales import Locale


def test_generic_attribute_access_and_provider_creation():
    """Generic should lazily create providers on attribute access."""
    g = Generic(locale=Locale.EN)
    # The first access should create an instance of the provider
    # and store it in the instance dict.
    provider_name = next(iter(g.__dir__()))  # pick any provider
    provider = getattr(g, provider_name)
    # After access, the provider should be stored in __dict__
    assert provider_name in g.__dict__
    # The provider should be an instance of BaseProvider
    assert isinstance(provider, BaseProvider)
    # Re-accessing should return the same instance (cached)
    provider_again = getattr(g, provider_name)
    assert provider is provider_again


def test_generic_reseed_propagates_to_providers():
    """Reseeding Generic should reseed all contained providers."""
    g = Generic(seed=123)
    # Pick a provider that has a reseed method
    provider_name = next(
        (name for name in g.__dir__() if hasattr(g, name) and hasattr(getattr(g, name), "reseed")),
        None,
    )
    assert provider_name is not None, "No provider with reseed method found"
    provider = getattr(g, provider_name)
    # Capture the provider's internal state before reseeding
    before_state = provider._random.randint(0, 1000)
    # Reseed Generic with a new seed
    g.reseed(456)
    # After reseeding, the provider should produce different sequence
    after_state = provider._random.randint(0, 1000)
    assert before_state != after_state, "Provider state did not change after reseeding"


def test_generic_add_provider_errors():
    """Adding an invalid provider should raise TypeError."""
    g = Generic()
    # Attempt to add a non-class object
    with pytest.raises(TypeError, match="The provider must be a class."):
        g.add_provider(42)

    # Attempt to add a class that is not a subclass of BaseProvider
    class NotAProvider:
        pass

    with pytest.raises(TypeError, match="The provider must be a subclass of"):
        g.add_provider(NotAProvider)

    # Attempt to add Generic itself
    with pytest.raises(TypeError, match="Cannot add Generic instance to itself."):
        g.add_provider(Generic)
