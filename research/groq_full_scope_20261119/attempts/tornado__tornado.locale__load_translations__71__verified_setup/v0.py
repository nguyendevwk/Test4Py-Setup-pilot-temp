import os
import csv
import codecs
import pytest
from tornado.locale import load_translations, _translations, _supported_locales, _default_locale

def test_load_translations_basic(tmp_path):
    # Create a simple CSV with two locales
    en_csv = tmp_path / "en_US.csv"
    es_csv = tmp_path / "es_ES.csv"
    en_csv.write_text('"Hello","Hola"\n', encoding="utf-8")
    es_csv.write_text('"Goodbye","Adiós"\n', encoding="utf-8")
    load_translations(str(tmp_path))
    # Check that translations dictionary contains both locales
    assert "en_US" in _translations
    assert "es_ES" in _translations
    # Verify that the English string maps correctly
    assert _translations["en_US"]["unknown"]["Hello"] == "Hola"
    assert _translations["es_ES"]["unknown"]["Goodbye"] == "Adiós"
    # Supported locales should include the default locale
    assert _default_locale in _supported_locales
    assert "en_US" in _supported_locales
    assert "es_ES" in _supported_locales

def test_load_translations_plural_and_missing_column(tmp_path):
    # CSV with plural indicator and missing third column
    csv_path = tmp_path / "fr_FR.csv"
    csv_path.write_text(
        '"%s likes this","%s aime ceci","plural"\n'
        '"%s likes this","%s aime ceci"\n',  # missing plural column
        encoding="utf-8"
    )
    load_translations(str(tmp_path))
    # The row with missing plural column should default to "unknown"
    assert _translations["fr_FR"]["plural"]["%s likes this"] == "%s aime ceci"
    assert _translations["fr_FR"]["unknown"]["%s likes this"] == "%s aime ceci"

def test_load_translations_invalid_plural_indicator(tmp_path, caplog):
    # CSV with an invalid plural indicator
    csv_path = tmp_path / "de_DE.csv"
    csv_path.write_text(
        '"Hello","Hallo","invalid"\n',
        encoding="utf-8"
    )
    load_translations(str(tmp_path))
    # The invalid row should be skipped; translations dict remains empty for this locale
    assert "de_DE" in _translations
    assert _translations["de_DE"] == {}
    # Check that an error was logged
    assert any(
        "Unrecognized plural indicator" in record.message
        for record in caplog.records
    )
