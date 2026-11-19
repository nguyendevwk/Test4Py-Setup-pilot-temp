import json
import pathlib
import pytest
from mimesis.providers.base import BaseDataProvider
from mimesis.enums import Locale
from mimesis.exceptions import LocaleError


class TestProvider(BaseDataProvider):
    class Meta:
        datafile = "test.json"
        datadir = pathlib.Path("")


def test_extract_and_update_dataset(tmp_path: pathlib.Path):
    # Prepare master locale file
    master_data = {"a": {"b": 1}}
    (tmp_path / "en").mkdir()
    (tmp_path / "en" / "test.json").write_text(json.dumps(master_data), encoding="utf8")

    # Prepare locale-specific file
    locale_data = {"a": {"c": 2}}
    (tmp_path / "en_US").mkdir()
    (tmp_path / "en_US" / "test.json").write_text(json.dumps(locale_data), encoding="utf8")

    # Instantiate provider with overridden datadir
    TestProvider.Meta.datadir = tmp_path
    provider = TestProvider(locale="en_US")

    # _extract should return nested value from merged data
    assert provider._extract(["a", "b"]) == 1
    assert provider._extract(["a", "c"]) == 2

    # Missing key returns default
    assert provider._extract(["a", "x"], default="missing") == "missing"

    # update_dataset merges new data
    provider.update_dataset({"a": {"d": 3}})
    assert provider._extract(["a", "d"]) == 3

    # _update_dict merges nested dicts correctly
    merged = provider._update_dict({"x": 1}, {"x": {"y": 2}})
    assert merged == {"x": {"y": 2}}


def test_extract_errors_and_update_dataset_type(tmp_path: pathlib.Path):
    # Prepare minimal datafile
    (tmp_path / "en").mkdir()
    (tmp_path / "en" / "test.json").write_text(json.dumps({"x": 1}), encoding="utf8")

    TestProvider.Meta.datadir = tmp_path
    provider = TestProvider(locale="en")

    # Empty keys raise ValueError
    with pytest.raises(ValueError, match="cannot be empty"):
        provider._extract([])

    # update_dataset with non-dict raises TypeError
    with pytest.raises(TypeError, match="must be a dict"):
        provider.update_dataset(["not", "a", "dict"])


def test_override_locale_context_manager_and_str(tmp_path: pathlib.Path):
    # Master locale
    (tmp_path / "en").mkdir()
    (tmp_path / "en" / "test.json").write_text(json.dumps({"msg": "hello"}), encoding="utf8")

    # French locale
    (tmp_path / "fr").mkdir()
    (tmp_path / "fr" / "test.json").write_text(json.dumps({"msg": "bonjour"}), encoding="utf8")

    TestProvider.Meta.datadir = tmp_path
    provider = TestProvider(locale="en")

    # Initial locale
    assert provider.get_current_locale() == "en"
    assert str(provider) == "TestProvider <en>"

    # Override locale within context
    with provider.override_locale(Locale.FR):
        assert provider.get_current_locale() == "fr"
        assert provider._extract(["msg"]) == "bonjour"

    # After context, locale restored
    assert provider.get_current_locale() == "en"
    assert provider._extract(["msg"]) == "hello"

    # Using an unsupported locale raises LocaleError via validate_locale
    with pytest.raises(LocaleError):
        provider.override_locale("unsupported")  # type: ignore[arg-type]
