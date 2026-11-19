import inspect
import pytest
from mimesis.providers.generic import Generic
from mimesis.providers.base import BaseProvider, BaseDataProvider
from mimesis.types import MissingSeed


class DummyProvider(BaseProvider):
    """Simple provider used only for testing."""

    class Meta:
        name = "dummy"

    def __init__(self, seed=MissingSeed, **kwargs):
        super().__init__(seed=seed)
        self.called = False

    def value(self):
        self.called = True
        return "dummy_value"


def test_generic_attribute_access_and_provider_instantiation():
    """Generic should lazily instantiate providers on first access."""
    g = Generic()
    # The DummyProvider is not registered, so it should not be present.
    assert not hasattr(g, "dummy")

    # Dynamically add DummyProvider to the registry for this test.
    # Since we cannot modify the registry, we add it via add_provider.
    g.add_provider(DummyProvider)
    # After adding, the provider should be accessible and callable.
    assert hasattr(g, "dummy")
    provider = g.dummy
    assert isinstance(provider, DummyProvider)
    # Calling a method should work and change internal state.
    assert provider.value() == "dummy_value"
    assert provider.called is True


def test_generic_reseed_propagates_to_providers():
    """Reseeding Generic should reseed all contained providers."""
    g = Generic()
    g.add_provider(DummyProvider)
    provider = g.dummy
    # Ensure provider has a seed attribute (inherited from BaseProvider).
    original_seed = provider.seed
    # Reseed Generic with a specific seed.
    g.reseed(12345)
    # The provider's seed should now match Generic's seed.
    assert provider.seed == 12345
    # Reseeding again with MissingSeed should reset to default behavior.
    g.reseed()
    assert provider.seed is MissingSeed


def test_generic_add_provider_errors_and_str_representation():
    """add_provider should raise TypeError for invalid inputs and __str__ works."""
    g = Generic()
    # Passing a non-class should raise TypeError.
    with pytest.raises(TypeError, match="must be a class"):
        g.add_provider(42)

    # Passing a class that is not a subclass of BaseProvider should raise TypeError.
    class NotAProvider:
        pass

    with pytest.raises(TypeError, match="must be a subclass"):
        g.add_provider(NotAProvider)

    # Adding Generic itself should raise TypeError.
    with pytest.raises(TypeError, match="Cannot add Generic instance"):
        g.add_provider(Generic)

    # __str__ should include class name and locale.
    assert str(g) == f"{g.__class__.__name__} <{g.locale}>"
