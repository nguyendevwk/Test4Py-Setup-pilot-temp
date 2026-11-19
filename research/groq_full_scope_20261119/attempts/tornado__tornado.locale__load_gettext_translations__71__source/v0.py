import os
import gettext
import tempfile
import shutil
import logging
import io
import sys
import importlib
import pytest
from pathlib import Path

# Import the target module
import tornado.locale as locale_module

# Helper to create a minimal .mo file for a given language
def create_mo_file(lang: str, domain: str, translations: dict, directory: Path):
    po_content = ""
    for msgid, msgstr in translations.items():
        po_content += f'msgid "{msgid}"\nmsgstr "{msgstr}"\n\n'
    po_path = directory / f"{lang}.po"
    po_path.write_text(po_content, encoding="utf-8")
    # Compile .po to .mo
    mo_path = directory / f"{lang}.mo"
    gettext.GNUTranslations.from_file(po_path.open("rb")).write(mo_path.open("wb"))
    return mo_path

@pytest.fixture
def locale_dir(tmp_path):
    """Create a temporary locale directory structure with a valid .mo file."""
    base = tmp_path / "locale"
    base.mkdir()
    lang_dir = base / "es" / "LC_MESSAGES"
    lang_dir.mkdir(parents=True)
    create_mo_file("es", "testdomain", {"hello": "hola"}, lang_dir)
    return base

def test_load_gettext_translations_success(locale_dir, caplog):
    """Verify that a valid .mo file is loaded and translations are available."""
    caplog.set_level(logging.DEBUG)
    locale_module.load_gettext_translations(str(locale_dir), "testdomain")
    # The global _translations should contain the 'es' entry
    assert hasattr(locale_module, "_translations")
    assert "es" in locale_module._translations
    # The translation should return the expected string
    trans = locale_module._translations["es"]
    assert trans.gettext("hello") == "hola"
    # Supported locales should include the default locale
    assert hasattr(locale_module, "_supported_locales")
    assert locale_module._default_locale in locale_module._supported_locales
    # Log should contain debug message about supported locales
    assert any("Supported locales" in rec.message for rec in caplog.records)

def test_load_gettext_translations_missing_file(tmp_path, caplog):
    """If no .mo files exist, no translations are loaded but function completes."""
    caplog.set_level(logging.DEBUG)
    locale_module.load_gettext_translations(str(tmp_path), "nonexistent")
    # No translations should be loaded
    assert hasattr(locale_module, "_translations")
    assert locale_module._translations == {}
    # Supported locales should only contain the default locale
    assert locale_module._supported_locales == frozenset([locale_module._default_locale])
    # No error logs should be present
    assert all(rec.levelno != logging.ERROR for rec in caplog.records)

def test_load_gettext_translations_invalid_file(tmp_path, caplog):
    """An invalid .mo file should be skipped with an error log."""
    # Create an invalid .mo file
    bad_dir = tmp_path / "bad" / "LC_MESSAGES"
    bad_dir.mkdir(parents=True)
    bad_file = bad_dir / "bad.mo"
    bad_file.write_bytes(b"not a valid mo file")
    caplog.set_level(logging.ERROR)
    locale_module.load_gettext_translations(str(tmp_path), "bad")
    # The invalid file should not be in translations
    assert "bad" not in locale_module._translations
    # An error log should be emitted
    assert any("Cannot load translation" in rec.message for rec in caplog.records)
