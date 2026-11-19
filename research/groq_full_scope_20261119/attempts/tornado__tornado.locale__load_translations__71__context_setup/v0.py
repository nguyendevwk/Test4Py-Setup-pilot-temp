import os
import csv
import pytest
from tornado.locale import load_translations, _translations, _supported_locales, _default_locale

def test_load_translations_basic(tmp_path):
    # Create a simple CSV with two locales
    csv_content = [
        ['"Hello"', '"Hola"'],
        ['"Goodbye"', '"Adiós"'],
    ]
    for locale in ['es_ES', 'fr_FR']:
        file_path = tmp_path / f"{locale}.csv"
        with open(file_path, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(csv_content)

    load_translations(str(tmp_path))
    # Verify that both locales are loaded
    assert _supported_locales == frozenset(['es_ES', 'fr_FR', _default_locale])
    # Verify translations for each locale
    for locale in ['es_ES', 'fr_FR']:
        assert _translations[locale]["unknown"]["Hello"] == "Hola"
        assert _translations[locale]["unknown"]["Goodbye"] == "Adiós"

def test_load_translations_plural_and_missing_column(tmp_path):
    # CSV with plural indicator and a row missing the third column
    csv_rows = [
        ['"Item"', '"Artículo"', 'plural'],
        ['"Item"', '"Artículo"', 'singular'],
        ['"Item"', '"Artículo"'],  # missing plural column
    ]
    file_path = tmp_path / "es_ES.csv"
    with open(file_path, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    load_translations(str(tmp_path))
    # Check that both plural and singular forms are stored
    assert _translations["es_ES"]["plural"]["Item"] == "Artículo"
    assert _translations["es_ES"]["singular"]["Item"] == "Artículo"
    # The row without a plural column should default to "unknown"
    assert _translations["es_ES"]["unknown"]["Item"] == "Artículo"

def test_load_translations_unrecognized_plural(tmp_path, caplog):
    # CSV with an invalid plural indicator
    csv_rows = [
        ['"Test"', '"Prueba"', 'invalid'],
    ]
    file_path = tmp_path / "es_ES.csv"
    with open(file_path, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    load_translations(str(tmp_path))
    # The invalid row should be skipped, leaving no translations
    assert "es_ES" not in _translations or not _translations["es_ES"]
    # An error should be logged
    assert any(
        "Unrecognized plural indicator" in record.message for record in caplog.records
    )
