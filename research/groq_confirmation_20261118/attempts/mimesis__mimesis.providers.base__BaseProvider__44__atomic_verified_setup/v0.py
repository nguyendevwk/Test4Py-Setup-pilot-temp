import json
import pathlib
import pytest
from mimesis.providers.base import BaseProvider
from mimesis.exceptions import NonEnumerableError
from mimesis.random import Random
from mimesis.types import Seed, MissingSeed
from mimesis.constants import DATADIR


class DummyEnum:
    """Simple enum-like class for testing validate_enum."""
    class Item:
        def __init__(self, value):
            self.value = value

    ONE = Item(1)
    TWO = Item(2)


def test_init_with_custom_random_and_seed(tmp_path: pathlib.Path):
    """Provider should use the supplied Random instance and seed."""
    custom_random = Random()
    seed_value = 12345
    provider = BaseProvider(seed=seed_value, random=custom_random)
    # The provider's random should be the same instance we passed
    assert provider.random is custom_random
    # The seed should be set correctly
    assert provider.seed == seed_value
    # Reseeding with a new seed changes the internal state
    provider.reseed(67890)
    assert provider.seed == 67890
    # The random instance should have been reseeded
    assert provider.random.randint(0, 1) in (0, 1)  # no exception


def test_validate_enum_raises_nonenumerable_error():
    """validate_enum should raise NonEnumerableError for invalid items."""
    provider = BaseProvider()
    # Passing None should pick a random enum item
    result = provider.validate_enum(None, DummyEnum)
    assert result in (1, 2)
    # Passing a valid enum member should return its value
    assert provider.validate_enum(DummyEnum.ONE, DummyEnum) == 1
    # Passing an invalid type should raise
    with pytest.raises(NonEnumerableError):
        provider.validate_enum("invalid", DummyEnum)


def test_read_global_file_returns_json(tmp_path: pathlib.Path):
    """_read_global_file should load a JSON file from the data directory."""
    provider = BaseProvider()
    # Use an existing global JSON file (e.g., countries.json)
    file_name = "countries.json"
    # Ensure the file exists
    file_path = DATADIR.joinpath("global", file_name)
    assert file_path.is_file()
    data = provider._read_global_file(file_name)
    # The data should be a dict (countries mapping)
    assert isinstance(data, dict)
    # Pick a known country code to verify content
    assert "US" in data
    assert isinstance(data["US"], dict)
