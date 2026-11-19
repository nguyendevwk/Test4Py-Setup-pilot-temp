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
def dummy_data(tmp_path):
    """Create a temporary data directory with a JSON file for DummyProvider."""
    data_dir = tmp_path / "data" / "en"
    data_dir.mkdir(parents=True)
    json_path = data_dir / "dummy.json"
    json.dump({"a": {"b": 1}}, json_path)
    # Patch the datadir to point to the temporary location
    DummyProvider.Meta.datadir = tmp_path / "data"
    return json_path


def test_extract_success_and_default(dummy_data):
    """Test that _extract returns correct nested value and default when missing."""
    provider = DummyProvider()
    # Existing path
    assert provider._extract(["a", "b"]) == 1
    # Missing path returns default
    assert provider._extract(["a", "c"], default="missing") == "missing"
    # Empty keys raise ValueError
    with pytest.raises(ValueError):
        provider._extract([])


def test_update_dataset_type_error(dummy_data):
    """Test that update_dataset raises TypeError when data is not a dict."""
    provider = DummyProvider()
    with pytest.raises(TypeError):
        provider.update_dataset(["not", "a", "dict"])


def test_override_locale_context_manager(dummy_data, tmp_path):
    """Test that override_locale temporarily changes locale and restores it."""
    provider = DummyProvider()
    original_locale = provider.get_current_locale()
    # Create a second locale file
    data_dir_fr = tmp_path / "data" / "fr"
    data_dir_fr.mkdir(parents=True)
    json_path_fr = data_dir_fr / "dummy.json"
    json.dump({"a": {"b": 2}}, json_path_fr)
    DummyProvider.Meta.datadir = tmp_path / "data"

    with provider.override_locale(Locale.FR):
        assert provider.get_current_locale() == "fr"
        assert provider._extract(["a", "b"]) == 2

    # After context, locale and data should be restored
    assert provider.get_current_locale() == original_locale
    assert provider._extract(["a", "b"]) == 1
