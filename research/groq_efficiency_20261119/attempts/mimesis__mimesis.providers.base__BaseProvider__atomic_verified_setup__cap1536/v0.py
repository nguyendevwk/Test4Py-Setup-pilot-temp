import json
import os
import tempfile
import types
import pytest
from mimesis.providers.base import BaseProvider
from mimesis.exceptions import NonEnumerableError
from mimesis.types import Seed, MissingSeed
from mimesis.random import Random
from mimesis.constants import DATADIR
from enum import Enum


# Helper: simple enum for testing validate_enum
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


def test_auto_register_subclass():
    """Subclassing BaseProvider should automatically register the provider."""
    class MyProvider(BaseProvider):
        class Meta:
            name = "my_provider"

    # The registry should contain the new provider under the given name
    registry = BaseProvider.__dict__.get("ProviderRegistry", None)
    assert registry is not None, "ProviderRegistry not found on BaseProvider"
    assert hasattr(registry, "providers"), "ProviderRegistry missing providers attribute"
    assert "my_provider" in registry.providers, "Provider not registered automatically"
    assert registry.providers["my_provider"] is MyProvider, "Registered provider mismatch"


def test_reseed_with_same_seed_generates_same_sequence(tmp_path: pathlib.Path):
    """Two providers with the same seed should produce identical random values."""
    seed_value = 12345
    provider_a = BaseProvider(seed=seed_value)
    provider_b = BaseProvider(seed=seed_value)

    # Generate a sequence of random integers from each provider
    seq_a = [provider_a.random.randint(0, 100) for _ in range(5)]
    seq_b = [provider_b.random.randint(0, 100) for _ in range(5)]

    assert seq_a == seq_b, "Sequences differ for same seed"

    # Reseed provider_a with a different seed and ensure sequences diverge
    provider_a.reseed(seed=seed_value + 1)
    seq_a_new = [provider_a.random.randint(0, 100) for _ in range(5)]
    assert seq_a_new != seq_b, "Sequences should differ after reseeding with a new seed"


def test_validate_enum_raises_nonenumerable_error():
    """validate_enum should raise NonEnumerableError when item is invalid."""
    provider = BaseProvider()
    # Passing an invalid item (not None, not enum instance) should raise
    with pytest.raises(NonEnumerableError) as excinfo:
        provider.validate_enum("invalid", Color)
    assert str(Color) in str(excinfo.value), "Error message should reference the enum type"
