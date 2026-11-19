import os
import gettext
import io
import struct
import pytest
from tornado.locale import load_gettext_translations, _supported_locales, _translations, _default_locale

def _create_mo_file(path, translations):
    """Create a minimal .mo file with the given translations dict."""
    # Build the binary .mo format
    # Header: magic, version, nstrings, orig_table, trans_table, hash, size
    # For simplicity, use 0 for hash and size
    nstrings = len(translations)
    # Offsets start after header (28 bytes)
    orig_offset = 28 + nstrings * 8
    trans_offset = orig_offset + sum(len(k.encode()) for k in translations) + nstrings * 4
    # Build tables
    orig_table = b""
    trans_table = b""
    orig_data = b""
    trans_data = b""
    for i, (msgid, msgstr) in enumerate(translations.items()):
        orig_len = len(msgid.encode())
        trans_len = len(msgstr.encode())
        orig_table += struct.pack("<II", orig_len, orig_offset + i * 4)
        trans_table += struct.pack("<II", trans_len, trans_offset + i * 4)
        orig_data += msgid.encode() + b"\0"
        trans_data += msgstr.encode() + b"\0"
    mo = struct.pack(
        "<IIIIIIII",
        0x950412de,  # magic
        0,          # version
        nstrings,
        28,         # orig_table offset
        28 + nstrings * 8,  # trans_table offset
        0,          # hash offset
        0,          # size offset
    )
    with open(path, "wb") as f:
        f.write(mo)
        f.write(orig_table)
        f.write(trans_table)
        f.write(orig_data)
        f.write(trans_data)

def test_load_gettext_translations_success(tmp_path):
    """Verify that valid .mo files are loaded and locales are registered."""
    domain = "testdomain"
    # Create two locale directories with valid .mo files
    for lang in ("en_US", "pt_BR"):
        lc_dir = tmp_path / lang / "LC_MESSAGES"
        lc_dir.mkdir(parents=True)
        mo_path = lc_dir / f"{domain}.mo"
        _create_mo_file(mo_path, {"hello": "hello" if lang == "en_US" else "olá"})
    load_gettext_translations(str(tmp_path), domain)
    # Check that both locales are present
    assert "en_US" in _translations
    assert "pt_BR" in _translations
    # Check that supported locales include default and the two
    assert _default_locale in _supported_locales
    assert "en_US" in _supported_locales
    assert "pt_BR" in _supported_locales
    # Verify that the translation works
    assert _translations["pt_BR"].gettext("hello") == "olá"

def test_load_gettext_translations_missing_lc_messages(tmp_path):
    """If LC_MESSAGES folder is missing, no translation should be loaded."""
    domain = "missingdomain"
    # Create a locale directory without LC_MESSAGES
    (tmp_path / "en_US").mkdir()
    load_gettext_translations(str(tmp_path), domain)
    # No translations should be loaded
    assert _translations == {}
    # Supported locales should only contain the default
    assert _supported_locales == frozenset([_default_locale])

def test_load_gettext_translations_invalid_file(tmp_path):
    """Corrupted .mo file should be skipped and not added to translations."""
    domain = "badomain"
    lc_dir = tmp_path / "en_US" / "LC_MESSAGES"
    lc_dir.mkdir(parents=True)
    bad_mo = lc_dir / f"{domain}.mo"
    # Write invalid content
    bad_mo.write_text("not a valid mo file")
    load_gettext_translations(str(tmp_path), domain)
    # The bad file should not be loaded
    assert "en_US" not in _translations
    # Supported locales should still include default only
    assert _supported_locales == frozenset([_default_locale])
