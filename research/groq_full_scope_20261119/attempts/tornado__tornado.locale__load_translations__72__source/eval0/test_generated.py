import os
import csv
import codecs
import importlib
import pytest
from tornado.locale import load_translations, _translations, _supported_locales, _default_locale

def test_load_translations_basic(tmp_path):
    # Create a simple CSV with two locales
    en_csv = tmp_path / "en_US.csv"
    es_csv = tmp_path / "es_ES.csv"
    en_csv.write_text('"Hello","Hola"\n', encoding='utf-8')
    es_csv.write_text('"Goodbye","Adiós"\n', encoding='utf-8')
    load_translations(str(tmp_path))
    # Check that translations are loaded correctly
    assert _translations["en_US"]["unknown"]["Hello"] == "Hola"
    assert _translations["es_ES"]["unknown"]["Goodbye"] == "Adiós"
    # Supported locales should include the two and the default
    assert _supported_locales == frozenset(["en_US", "es_ES", _default_locale])

def test_load_translations_plural_and_encoding(tmp_path):
    # Create a UTF-16 LE encoded CSV with plural indicators
    csv_path = tmp_path / "fr_FR.csv"
    rows = [
        ['"Item","Article"', 'unknown'],
        ['"%(name)s liked this","Un %(name)s a aimé ceci","plural"'],
        ['"%(name)s liked this","Un %(name)s a aimé ceci","singular"'],
    ]
    # Write with BOM for UTF-16 LE
    with open(csv_path, 'wb') as f:
        f.write(codecs.BOM_UTF16_LE)
        writer = csv.writer(f, dialect='excel')
        for row in rows:
            writer.writerow(row)
    load_translations(str(tmp_path))
    # Verify plural forms stored correctly
    assert _translations["fr_FR"]["plural"]["%(name)s liked this"] == "Un %(name)s a aimé ceci"
    assert _translations["fr_FR"]["singular"]["%(name)s liked this"] == "Un %(name)s a aimé ceci"
    # Ensure encoding detection worked (no error raised)
    assert "fr_FR" in _translations

def test_load_translations_invalid_plural(tmp_path, caplog):
    # Create a CSV with an invalid plural indicator
    bad_csv = tmp_path / "de_DE.csv"
    bad_csv.write_text('"Test","Testen","invalid"\n', encoding='utf-8')
    load_translations(str(tmp_path))
    # The invalid row should be skipped; no translation stored
    assert "de_DE" not in _translations or "unknown" not in _translations.get("de_DE", {})
    # Check that an error was logged
    assert any("Unrecognized plural indicator" in rec.message for rec in caplog.records)
