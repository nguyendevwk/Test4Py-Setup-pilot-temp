import json
import os
import types
import pytest
from mimesis.providers.base import BaseProvider
from mimesis.exceptions import NonEnumerableError
from mimesis import random as _random
from mimesis.constants import DATADIR

# Helper enum for testing validate_enum
class DummyEnum:
    class Item:
        def __init__(self, value):
            self.value = value
    ONE = Item(1)
    TWO = Item(2)

# ---------------------------------------------------------------------------

def test_auto_register_subclass(tmp_path):
    """
    Verify that a subclass of BaseProvider with Meta.name is automatically
    registered in ProviderRegistry when auto_register is True.
    """
    # Create a dummy registry module with a register function
    registry = types.SimpleNamespace()
    registry.registered = {}
    def register(name, cls):
        registry.registered[name] = cls
    registry.register = register

    # Monkeypatch the global ProviderRegistry
    original_registry = BaseProvider.__dict__.get('ProviderRegistry', None)
    BaseProvider.ProviderRegistry = registry

    class MyProvider(BaseProvider):
        class Meta:
            name = "my_provider"

    # The subclass should have been registered during class creation
    assert "my_provider" in registry.registered
    assert registry.registered["my_provider"] is MyProvider

    # Clean up
    if original_registry is not None:
        BaseProvider.ProviderRegistry = original_registry
    else:
        delattr(BaseProvider, 'ProviderRegistry')


def test_reseed_with_global_seed(tmp_path):
    """
    Verify that reseeding with MissingSeed uses the global seed
    and that two providers with the same global seed produce identical
    random values.
    """
    # Set a deterministic global seed
    _random.global_seed = 12345

    provider1 = BaseProvider(seed=_random.MissingSeed)
    provider2 = BaseProvider(seed=_random.MissingSeed)

    # Both should use the same global seed
    assert provider1.seed is _random.MissingSeed
    assert provider2.seed is _random.MissingSeed

    # Generate a random number from each provider
    val1 = provider1.random.randint(0, 100)
    val2 = provider2.random.randint(0, 100)

    # Because they share the same global seed, the numbers should match
    assert val1 == val2

    # Now reseed provider1 with a different seed and ensure values diverge
    provider1.reseed(999)
    val3 = provider1.random.randint(0, 100)
    assert val3 != val2


def test_validate_enum_raises_on_invalid_item(tmp_path):
    """
    Verify that validate_enum raises NonEnumerableError when the item is
    not part of the enum and not None.
    """
    provider = BaseProvider()
    # Passing an invalid item (e.g., a string) should raise
    with pytest.raises(NonEnumerableError):
        provider.validate_enum("invalid", DummyEnum)

    # Passing None should return a random enum item value
    result = provider.validate_enum(None, DummyEnum)
    assert result in (1, 2)

    # Passing a valid enum member should return its value
    assert provider.validate_enum(DummyEnum.ONE, DummyEnum) == 1
