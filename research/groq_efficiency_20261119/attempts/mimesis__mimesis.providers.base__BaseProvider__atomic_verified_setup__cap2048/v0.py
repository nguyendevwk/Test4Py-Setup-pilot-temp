import json
import os
import pytest
from mimesis.providers.base import BaseProvider
from mimesis.exceptions import NonEnumerableError
from mimesis.types import Seed, MissingSeed
from mimesis.random import Random
from enum import Enum

class DummyEnum(Enum):
    A = 1
    B = 2

def test_init_with_invalid_random_raises_type_error():
    """Providing a non‑Random instance to BaseProvider should raise TypeError."""
    with pytest.raises(TypeError, match="random must be an instance of mimesis.random.Random"):
        BaseProvider(random="not a Random instance")

def test_validate_enum_returns_value_and_raises_on_invalid():
    """validate_enum should return the enum value or raise NonEnumerableError."""
    provider = BaseProvider()
    # Valid enum member
    assert provider.validate_enum(DummyEnum.A, DummyEnum) == DummyEnum.A.value
    # None should pick a random enum member
    result = provider.validate_enum(None, DummyEnum)
    assert result in (DummyEnum.A.value, DummyEnum.B.value)
    # Invalid type should raise
    with pytest.raises(NonEnumerableError):
        provider.validate_enum("invalid", DummyEnum)

def test_read_global_file_missing_raises_file_not_found(tmp_path):
    """Attempting to read a non‑existent global file should raise FileNotFoundError."""
    provider = BaseProvider()
    # Construct a file name that is guaranteed not to exist
    missing_file = "this_file_does_not_exist.json"
    # Ensure the file does not exist in the data directory
    data_dir = provider._read_global_file.__globals__["DATADIR"]
    full_path = data_dir.joinpath("global", missing_file)
    if full_path.exists():
        os.remove(full_path)
    with pytest.raises(FileNotFoundError):
        provider._read_global_file(missing_file)
