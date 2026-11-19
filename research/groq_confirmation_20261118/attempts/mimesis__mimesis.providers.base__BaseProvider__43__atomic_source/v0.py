import json
import types
import pytest
from mimesis.providers.base import BaseProvider
from mimesis.exceptions import NonEnumerableError
from mimesis.random import Random
from mimesis.constants import DATADIR
from mimesis.types import Seed, MissingSeed


class DummyEnum:
    """Simple enum-like class for testing validate_enum."""
    class Item:
        def __init__(self, value):
            self.value = value

    ONE = Item(1)
    TWO = Item(2)


def test_init_with_custom_random_and_reseed(tmp_path):
    """Test that providing a custom Random instance works and reseeding behaves correctly."""
    # Create a custom Random instance with a known seed
    custom_random = Random(seed=123)
    provider = BaseProvider(random=custom_random, seed=456)

    # The provider should use the custom Random instance
    assert provider.random is custom_random

    # The seed should be set to 456
    assert provider.seed == 456

    # Reseed with a new seed and verify the internal state changes
    provider.reseed(789)
    assert provider.seed == 789
    # The underlying Random should now be seeded with 789
    assert provider.random.randint(0, 1) in (0, 1)  # just ensure no exception


def test_validate_enum_raises_non_enumerable_error():
    """Test that validate_enum raises NonEnumerableError for invalid items."""
    provider = BaseProvider()
    # Passing an invalid item should raise the custom exception
    with pytest.raises(NonEnumerableError) as excinfo:
        provider.validate_enum("invalid", DummyEnum)
    assert str(excinfo.value) == str(DummyEnum)


def test_has_seed_logic(tmp_path):
    """Test the internal _has_seed method for various seed configurations."""
    provider = BaseProvider()

    # No seed set and global seed is None
    provider.seed = MissingSeed
    Random.global_seed = None
    assert not provider._has_seed()

    # Seed set to a concrete value
    provider.seed = 42
    Random.global_seed = None
    assert provider._has_seed()

    # Seed set to MissingSeed but global seed is set
    provider.seed = MissingSeed
    Random.global_seed = 99
    assert provider._has_seed()

    # Both provider and global seed are MissingSeed
    provider.seed = MissingSeed
    Random.global_seed = MissingSeed
    assert not provider._has_seed()
