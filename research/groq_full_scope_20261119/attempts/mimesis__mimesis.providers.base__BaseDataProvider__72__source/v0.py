import json
import pathlib
import pytest
from mimesis.providers.base import BaseDataProvider
from mimesis.locales import Locale
from mimesis.constants import DATADIR, LOCALE_SEP


class DummyProvider(BaseDataProvider):
    class Meta:
        datafile = "dummy.json"
        datadir = None  # will be set in tests


def test_extract_and_update_dict(tmp_path: pathlib.Path):
    # Prepare a nested JSON dataset
    data = {"a": {"b": {"c": 1}}, "x": 2}
    (tmp_path / "en" / "dummy.json").mkdir(parents=True)
    (tmp_path / "en" / "dummy.json").write_text(json.dumps(data), encoding="utf8")

    DummyProvider.Meta.datadir = tmp_path
    provider = DummyProvider(locale="en")

    # _extract should return nested value
    assert provider._extract(["a", "b", "c"]) == 1
    # Missing key returns default
    assert provider._extract(["a", "z"], default="missing") == "missing"

    # _update_dict merges nested dicts
    new = {"a": {"b": {"d": 3}}, "y": 4}
    merged = provider._update_dict(provider._dataset.copy(), new)
    assert merged == {"a": {"b": {"c": 1, "d": 3}}, "x": 2, "y": 4}


def test_update_dataset_and_str(tmp_path: pathlib.Path):
    # Base dataset
    base = {"foo": "bar"}
    (tmp_path / "en" / "dummy.json").mkdir(parents=True)
    (tmp_path / "en" / "dummy.json").write_text(json.dumps(base), encoding="utf8")

    DummyProvider.Meta.datadir = tmp_path
    provider = DummyProvider(locale="en")

    # update_dataset should merge dict
    provider.update_dataset({"foo": "baz", "new": 123})
    assert provider._dataset["foo"] == "baz"
    assert provider._dataset["new"] == 123

    # __str__ should reflect locale
    assert str(provider) == f"{provider.__class__.__name__} <{Locale('en')}>"


def test_override_locale_context_manager(tmp_path: pathlib.Path):
    # Master locale data
    en_data = {"greeting": "Hello"}
    # Specific locale data
    fr_data = {"greeting": "Bonjour"}

    (tmp_path / "en" / "dummy.json").mkdir(parents=True)
    (tmp_path / "en" / "dummy.json").write_text(json.dumps(en_data), encoding="utf8")
    (tmp_path / "fr" / "dummy.json").mkdir(parents=True)
    (tmp_path / "fr" / "dummy.json").write_text(json.dumps(fr_data), encoding="utf8")

    DummyProvider.Meta.datadir = tmp_path
    provider = DummyProvider(locale="en")

    # Initially uses English greeting
    assert provider._extract(["greeting"]) == "Hello"

    # Override locale temporarily
    with provider.override_locale(Locale("fr")):
        assert provider._extract(["greeting"]) == "Bonjour"

    # After context, locale restored to English
    assert provider._extract(["greeting"]) == "Hello"
