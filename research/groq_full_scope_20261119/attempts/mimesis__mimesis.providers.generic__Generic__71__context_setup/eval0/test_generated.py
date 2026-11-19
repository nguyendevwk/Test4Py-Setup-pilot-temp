import pytest
from mimesis.providers.generic import Generic
from mimesis.providers.base import BaseProvider
from mimesis.types import MissingSeed


class DummyProvider(BaseProvider):
    """Simple provider used only for testing."""

    class Meta:
        name = "dummy"

    def __init__(self, seed=MissingSeed):
        super().__init__(seed=seed)
        self.counter = 0

    def increment(self):
        self.counter += 1
        return self.counter


def test_generic_attribute_access_and_reseed(tmp_path):
    """Test that Generic lazily creates provider instances and reseeds them."""
    g = Generic()
    # Access the dummy provider via attribute; it should be created lazily
    dummy = g.dummy
    assert isinstance(dummy, DummyProvider)
    # The provider should use the same seed as Generic
    assert dummy.seed == g.seed

    # Call a method to change internal state
    assert dummy.increment() == 1
    assert dummy.increment() == 2

    # Reseed Generic and ensure provider's seed is updated
    g.reseed(12345)
    assert g.seed == 12345
    assert dummy.seed == 12345
    # After reseed, counter should reset because DummyProvider's __init__ sets counter to 0
    assert dummy.counter == 0


def test_generic_add_provider_and_error_handling():
    """Test adding a provider and error cases for add_provider."""
    g = Generic()

    # Adding a valid provider class should succeed
    g.add_provider(DummyProvider)
    assert hasattr(g, "dummy")
    assert isinstance(g.dummy, DummyProvider)

    # Adding a non-class should raise TypeError
    with pytest.raises(TypeError, match="The provider must be a class."):
        g.add_provider("not_a_class")

    # Adding a class that is not a subclass of BaseProvider should raise TypeError
    class NotProvider:
        pass

    with pytest.raises(TypeError, match="The provider must be a subclass of"):
        g.add_provider(NotProvider)

    # Adding Generic itself should raise TypeError
    with pytest.raises(TypeError, match="Cannot add Generic instance to itself."):
        g.add_provider(Generic)


def test_generic_str_representation():
    """Test that __str__ returns the expected human‑readable representation."""
    g = Generic(locale="fr")
    assert str(g) == "Generic <fr>"
