import enum
import json
import os
import tempfile
import pytest
from mimesis.providers.base import BaseProvider
from mimesis.exceptions import NonEnumerableError
from mimesis import random as _random


class DummyProvider(BaseProvider):
    """Simple provider exposing the underlying random instance."""

    def random_int(self, a: int, b: int) -> int:
        return self.random.randint(a, b)


def test_reseed_same_seed_generates_same_sequence(tmp_path):
    """Two providers with the same seed produce identical random numbers."""
    seed = 12345
    provider1 = DummyProvider(seed=seed)
    provider2 = DummyProvider(seed=seed)

    # Generate a sequence of random integers from each provider
    seq1 = [provider1.random_int(1, 100) for _ in range(5)]
    seq2 = [provider2.random_int(1, 100) for _ in range(5)]

    assert seq1 == seq2, "Sequences should be identical for the same seed"


def test_validate_enum_raises_on_invalid_item():
    """validate_enum should raise NonEnumerableError when item is not a member of the enum."""
    class Color(enum.Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

    provider = DummyProvider()
    with pytest.raises(NonEnumerableError) as excinfo:
        provider.validate_enum("YELLOW", Color)

    assert str(excinfo.value) == str(Color), "Error message should contain the enum type"


def test_read_global_file_raises_file_not_found(tmp_path):
    """_read_global_file should raise FileNotFoundError for missing files."""
    provider = DummyProvider()
    missing_file = "nonexistent.json"

    with pytest.raises(FileNotFoundError):
        provider._read_global_file(missing_file)
