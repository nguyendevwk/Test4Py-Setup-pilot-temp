import os
import csv
import codecs
import pytest
from tornado.locale import load_translations, _translations, _supported_locales, _default_locale

def test_load_translations_normal(tmp_path):
    # Create a valid CSV file for locale 'es_GT'
    csv_path = tmp_path / "es_GT.csv"
    csv_path.write_text(
        '"Hello","Hola"\n'
        '"Goodbye","Adiós"\n',
        encoding="utf-8",
    )
    load_translations(str(tmp_path))
    # Verify that the locale is loaded with default plural indicator
    assert "es_GT" in _translations
    assert _translations["es_GT"]["unknown"]["Hello"] == "Hola"
    assert _translations["es_GT"]["unknown"]["Goodbye"] == "Adiós"
    # Supported locales should include the default locale
    assert _default_locale in _supported_locales
    assert "es_GT" in _supported_locales

def test_load_translations_plural_and_bom(tmp_path):
    # Create a UTF-16 LE encoded CSV with plural indicators
    csv_path = tmp_path / "fr_FR.csv"
    data = (
        '"%s liked this","%s a aimé ceci","plural"\n'
        '"%s liked this","%s a aimé ceci","singular"\n'
    )
    # Write with BOM for UTF-16 LE
    with open(csv_path, "wb") as f:
        f.write(codecs.BOM_UTF16_LE)
        f.write(data.encode("utf-16-le"))
    load_translations(str(tmp_path))
    # Verify that both plural and singular forms are stored
    assert "fr_FR" in _translations
    assert _translations["fr_FR"]["plural"]["%s liked this"] == "%s a aimé ceci"
    assert _translations["fr_FR"]["singular"]["%s liked this"] == "%s a aimé ceci"

def test_load_translations_invalid_locale(tmp_path, caplog):
    # Create a CSV file with an invalid locale name
    csv_path = tmp_path / "invalid-locale.csv"
    csv_path.write_text('"Test","Prueba"\n', encoding="utf-8")
    load_translations(str(tmp_path))
    # The invalid file should be skipped, so no locale added
    assert "invalid-locale" not in _translations
    # An error should be logged
    assert any(
        record.message.startswith("Unrecognized locale")
        for record in caplog.records
    )
