import enum
import json
import os
import tempfile
import types
import pytest

from mimesis.providers.base import BaseProvider
from mimesis import random as _random
from mimesis.exceptions import NonEnumerableError


class DummyProvider(BaseProvider):
    class Meta:
        name = "dummy"
        auto_register = True


def test_auto_register_registry():
    """Provider should be automatically registered in the registry."""
    # The registry is a global dict in mimesis.providers.registry
    from mimesis.providers.registry import ProviderRegistry
    assert "dummy" in ProviderRegistry._registry
    assert ProviderRegistry._registry["dummy"] is DummyProvider


def test_reseed_with_missing_seed_uses_global_seed(tmp_path):
    """When seed is MissingSeed, reseed uses the global seed."""
    # Create a temporary file to act as a seed source
    seed_file = tmp_path / "seed.txt"
    seed_file.write_text("12345")

    # Set global seed
    _random.global_seed = 98765
    provider = DummyProvider(seed=MissingSeed)
    # The provider's internal random should be seeded with global seed
    assert provider.random.randint(0, 100) == provider.random.randint(0, 100)

    # Now reseed with a specific seed
    provider.reseed(42)
    assert provider.random.randint(0, 100) != provider.random.randint(0, 100)


def test_validate_enum_raises_on_invalid_item():
    """validate_enum should raise NonEnumerableError for invalid items."""
    class Color(enum.Enum):
        RED = 1
        GREEN = 2

    provider = DummyProvider()
    with pytest.raises(NonEnumerableError):
        provider.validate_enum("BLUE", Color)
