import json
import pathlib
import pytest
from mimesis.providers.base import BaseDataProvider
from mimesis.locales import Locale
from mimesis.constants import DATADIR, LOCALE_SEP


class DummyProvider(BaseDataProvider):
    class Meta:
        datafile = "dummy.json"
        datadir = pathlib.Path("dummy_datadir")


@pytest.fixture
def setup_dummy_datadir(tmp_path):
    """Create a temporary data directory with locale JSON files."""
    datadir = tmp_path / "dummy_datadir"
    datadir.mkdir()
    # Master locale file
    master = datadir / "en" / "dummy.json"
    master.parent.mkdir(parents=True, exist_ok=True)
    master.write_text(json.dumps({"key": {"sub": 1}}), encoding="utf8")
    # Specific locale file
    specific = datadir / "en_US" / "dummy.json"
    specific.parent.mkdir(parents=True, exist_ok=True)
    specific.write_text(json.dumps({"key": {"sub": 2, "extra": 3}}), encoding="utf8")
    return datadir


def test_extract_and_update_dataset(setup_dummy_datadir):
    """Test nested extraction and dataset update."""
    provider = DummyProvider(locale="en_US", datadir=setup_dummy_datadir)
    # Extraction of existing nested key
    assert provider._extract(["key", "sub"]) == 2
    # Extraction with default for missing key
    assert provider._extract(["key", "missing"], default="fallback") == "fallback"
    # Update dataset with new key
    provider.update_dataset({"new": {"value": 42}})
    assert provider._extract(["new", "value"]) == 42
    # Update dataset with existing key overrides
    provider.update_dataset({"key": {"sub": 99}})
    assert provider._extract(["key", "sub"]) == 99


def test_override_locale_context_manager(setup_dummy_datadir):
    """Test temporary locale override using context manager."""
    provider = DummyProvider(locale="en", datadir=setup_dummy_datadir)
    assert provider._extract(["key", "sub"]) == 1
    with provider.override_locale(Locale("en_US")):
        # Inside context, locale should be overridden
        assert provider._extract(["key", "sub"]) == 2
        assert provider._extract(["key", "extra"]) == 3
    # After context, locale should revert
    assert provider._extract(["key", "sub"]) == 1
    assert provider._extract(["key", "extra"]) is None


def test_invalid_update_and_extract_errors(setup_dummy_datadir):
    """Test error handling for invalid inputs."""
    provider = DummyProvider(locale="en", datadir=setup_dummy_datadir)
    # update_dataset should raise TypeError for non-dict
    with pytest.raises(TypeError, match="The data must be a dict."):
        provider.update_dataset(["not", "a", "dict"])
    # _extract should raise ValueError for empty key list
    with pytest.raises(ValueError, match="The list of keys to extract cannot be empty."):
        provider._extract([])
