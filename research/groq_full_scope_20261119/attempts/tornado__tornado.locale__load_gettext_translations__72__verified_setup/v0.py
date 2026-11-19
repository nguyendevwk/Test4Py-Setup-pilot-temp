import os
import gettext
import tempfile
import shutil
import io
import struct
import sys
import importlib
import pytest
from pathlib import Path

# Import the target module
import tornado.locale as locale_module

# Helper to create a minimal .mo file for a given language
def create_mo_file(directory: Path, lang: str, domain: str, translations: dict):
    lc_messages = directory / lang / "LC_MESSAGES"
    lc_messages.mkdir(parents=True, exist_ok=True)
    mo_path = lc_messages / f"{domain}.mo"

    # Build a minimal binary .mo file
    # Header: magic, revision, nstrings, orig_table, trans_table, hash, size, offset
    # For simplicity, we use only one string
    nstrings = len(translations)
    # Offsets
    orig_offset = 28 + nstrings * 8
    trans_offset = orig_offset + sum(len(k.encode("utf-8")) + 1 for k in translations.keys())
    # Build tables
    orig_table = b""
    trans_table = b""
    for i, (orig, trans) in enumerate(translations.items()):
        orig_table += struct.pack("<II", len(orig), orig_offset + i * 8)
        trans_table += struct.pack("<II", len(trans), trans_offset + i * 8)
    # Build strings
    orig_strings = b"".join(k.encode("utf-8") + b"\0" for k in translations.keys())
    trans_strings = b"".join(v.encode("utf-8") + b"\0" for v in translations.values())
    # Header
    header = struct.pack("<IIIIIIII", 0x950412de, 0, nstrings, orig_offset, trans_offset, 0, 0, 0)
    mo_content = header + orig_table + trans_table + orig_strings + trans_strings
    mo_path.write_bytes(mo_content)

# Test that load_gettext_translations correctly loads valid .mo files
def test_load_gettext_translations_success(tmp_path: Path):
    domain = "testdomain"
    # Create two language directories with valid .mo files
    create_mo_file(tmp_path, "en", domain, {"Hello": "Hello"})
    create_mo_file(tmp_path, "es", domain, {"Hello": "Hola"})
    # Load translations
    locale_module.load_gettext_translations(str(tmp_path), domain)
    # Verify internal state
    assert hasattr(locale_module, "_translations")
    assert "en" in locale_module._translations
    assert "es" in locale_module._translations
    # Check that translations work
    trans_en = locale_module._translations["en"].gettext("Hello")
    trans_es = locale_module._translations["es"].gettext("Hello")
    assert trans_en == "Hello"
    assert trans_es == "Hola"
    # Supported locales should include default locale
    assert locale_module._default_locale in locale_module._supported_locales
    assert "en" in locale_module._supported_locales
    assert "es" in locale_module._supported_locales

# Test that load_gettext_translations skips invalid .mo files and logs an error
def test_load_gettext_translations_invalid_file(tmp_path: Path, caplog):
    domain = "testdomain"
    # Create a valid .mo file
    create_mo_file(tmp_path, "fr", domain, {"Hello": "Bonjour"})
    # Create an invalid .mo file (empty file)
    (tmp_path / "de" / "LC_MESSAGES").mkdir(parents=True, exist_ok=True)
    (tmp_path / "de" / "LC_MESSAGES" / f"{domain}.mo").write_bytes(b"")
    # Load translations
    locale_module.load_gettext_translations(str(tmp_path), domain)
    # The invalid file should be skipped; only 'fr' should be loaded
    assert "fr" in locale_module._translations
    assert "de" not in locale_module._translations
    # Check that an error was logged
    error_logs = [rec for rec in caplog.records if rec.levelname == "ERROR"]
    assert any("Cannot load translation for 'de'" in rec.getMessage() for rec in error_logs)

# Test that load_gettext_translations handles missing directory gracefully
def test_load_gettext_translations_missing_directory(tmp_path: Path, caplog):
    domain = "testdomain"
    # Directory does not contain any locale subdirectories
    locale_module.load_gettext_translations(str(tmp_path), domain)
    # No translations should be loaded
    assert locale_module._translations == {}
    # Supported locales should only contain the default locale
    assert locale_module._supported_locales == frozenset([locale_module._default_locale])
    # No error logs should be present
    assert not any(rec.levelname == "ERROR" for rec in caplog.records)
