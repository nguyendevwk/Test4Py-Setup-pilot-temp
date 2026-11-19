import os
import csv
import pytest
from tornado.locale import load_translations, _translations, _supported_locales, _default_locale

def test_load_translations_basic(tmp_path):
    # Create a simple CSV with two locales
    csv_content = """\
"I love you","Te amo"
"%(name)s liked this","A %(name)s les gustó esto","plural"
"%(name)s liked this","A %(name)s le gustó esto","singular"
"""
    (tmp_path / "es_GT.csv").write_text(csv_content, encoding="utf-8-sig")
    (tmp_path / "fr_FR.csv").write_text(csv_content, encoding="utf-8-sig")
    load_translations(str(tmp_path))
    # Check that both locales are loaded
    assert "es_GT" in _translations
    assert "fr_FR" in _translations
    # Check that the translations dictionary contains the expected keys
    assert _translations["es_GT"]["plural"]["I love you"] == "Te amo"
    assert _translations["es_GT"]["plural"]["%(name)s liked this"] == "A %(name)s les gustó esto"
    assert _translations["es_GT"]["singular"]["%(name)s liked this"] == "A %(name)s le gustó esto"
    # Supported locales should include the default and the two new ones
    assert _supported_locales == frozenset(["en_US", "es_GT", "fr_FR"])

def test_load_translations_missing_plural_column(tmp_path):
    # CSV with only two columns (no plural indicator)
    csv_content = """\
"Hello","Hola"
"""
    (tmp_path / "es_ES.csv").write_text(csv_content, encoding="utf-8-sig")
    load_translations(str(tmp_path))
    # The missing plural column defaults to "unknown"
    assert _translations["es_ES"]["unknown"]["Hello"] == "Hola"
    # Supported locales should include the default and the new one
    assert _supported_locales == frozenset(["en_US", "es_ES"])

def test_load_translations_invalid_locale(tmp_path, caplog):
    # CSV file with an invalid locale name
    csv_content = """\
"Good morning","Buenos días"
"""
    (tmp_path / "invalid-locale.csv").write_text(csv_content, encoding="utf-8-sig")
    load_translations(str(tmp_path))
    # No new locale should be added
    assert "invalid-locale" not in _translations
    # The error should be logged
    assert any(
        "Unrecognized locale" in record.message and "invalid-locale.csv" in record.message
        for record in caplog.records
    )
