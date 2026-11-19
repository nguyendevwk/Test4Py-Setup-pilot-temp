import json
import pathlib
import pytest
from mimesis.providers.base import BaseDataProvider
from mimesis.enums import Locale


class DummyProvider(BaseDataProvider):
    class Meta:
        name = "dummy"
        datafile = "dummy.json"
        datadir = pathlib.Path(__file__).parent / "data"


@pytest.fixture
def dummy_provider(tmp_path):
    # Create a minimal data file for the dummy provider
    data_dir = tmp_path / "en"
    data_dir.mkdir(parents=True)
    (data_dir / "dummy.json").write_text(json.dumps({"a": {"b": 1}}))
    # Patch the provider's Meta.datadir to point to tmp_path
    DummyProvider.Meta.datadir = tmp_path
    return DummyProvider()


def test_extract_missing_keys_raises(dummy_provider):
    # _extract should raise ValueError when keys list is empty
    with pytest.raises(ValueError, match="cannot be empty"):
        dummy_provider._extract([])


def test_update_dataset_type_error(dummy_provider):
    # update_dataset must receive a dict
    with pytest.raises(TypeError, match="must be a dict"):
        dummy_provider.update_dataset(["not", "a", "dict"])


def test_override_locale_context_manager(dummy_provider, tmp_path):
    # Create a second locale file
    data_dir_fr = tmp_path / "fr"
    data_dir_fr.mkdir(parents=True)
    (data_dir_fr / "dummy.json").write_text(json.dumps({"a": {"b": 2}}))
    DummyProvider.Meta.datadir = tmp_path

    # Reload dataset for initial locale
    dummy_provider._load_dataset()
    assert dummy_provider._extract(["a", "b"]) == 1

    # Use context manager to switch locale
    with dummy_provider.override_locale(Locale.FR):
        assert dummy_provider._extract(["a", "b"]) == 2

    # After exiting, locale should revert
    assert dummy_provider._extract(["a", "b"]) == 1
