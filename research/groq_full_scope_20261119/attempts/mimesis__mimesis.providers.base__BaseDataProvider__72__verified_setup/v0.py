import json
import pathlib
import pytest
from mimesis.providers.base import BaseDataProvider
from mimesis.enums import Locale
from mimesis.exceptions import NonEnumerableError

# Create a minimal concrete provider for testing
class TestProvider(BaseDataProvider):
    class Meta:
        datafile = "test.json"
        datadir = pathlib.Path(__file__).parent / "data"

@pytest.fixture
def provider(tmp_path):
    # Prepare a data directory with a JSON file for the default locale
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "en").mkdir()
    (data_dir / "en" / "test.json").write_text(
        json.dumps({"a": {"b": 1}, "c": 2})
    )
    # Patch the provider's datadir to point to the temporary directory
    TestProvider.Meta.datadir = data_dir
    return TestProvider()

def test_extract_and_update_dataset(provider):
    # Normal extraction
    assert provider._extract(["a", "b"]) == 1
    # Missing key returns default
    assert provider._extract(["a", "x"], default="missing") == "missing"
    # Empty key list raises ValueError
    with pytest.raises(ValueError):
        provider._extract([])
    # Update dataset with a new key
    provider.update_dataset({"d": 4})
    assert provider._extract(["d"]) == 4
    # Updating with non-dict raises TypeError
    with pytest.raises(TypeError):
        provider.update_dataset(["not", "a", "dict"])

def test_override_locale_context_manager(tmp_path):
    # Create data for two locales
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    for loc in ("en", "fr"):
        (data_dir / loc).mkdir()
        (data_dir / loc / "test.json").write_text(
            json.dumps({"lang": loc})
        )
    TestProvider.Meta.datadir = data_dir
    provider = TestProvider()
    # Default locale
    assert provider.get_current_locale() == "en"
    # Override locale temporarily
    with provider.override_locale(Locale.FR):
        assert provider.get_current_locale() == "fr"
        assert provider._extract(["lang"]) == "fr"
    # After context, locale restored
    assert provider.get_current_locale() == "en"
    assert provider._extract(["lang"]) == "en"

def test_str_representation_and_invalid_override():
    provider = TestProvider()
    # __str__ includes class name and locale
    assert str(provider) == f"TestProvider <{Locale.EN}>"
    # Attempt to override with an invalid locale (not a Locale enum)
    with pytest.raises(ValueError):
        provider.override_locale("invalid")  # type: ignore[arg-type]
