import os
import glob
import gettext
import tempfile
import shutil
import io
import struct
import pytest
from tornado.locale import load_gettext_translations, _supported_locales, _translations, _use_gettext, _default_locale

def _create_mo_file(path, msgid, msgstr):
    """
    Create a minimal .mo file containing a single translation entry.
    """
    # Build the .mo file header and tables
    # Header: magic, revision, nstrings, orig_offset, trans_offset, hash_offset
    magic = 0x950412de
    revision = 0
    nstrings = 1
    # Offsets will be calculated after building tables
    # Build original and translation tables
    orig = msgid.encode('utf-8') + b'\x00'
    trans = msgstr.encode('utf-8') + b'\x00'
    orig_len = len(orig)
    trans_len = len(trans)
    # Offsets for strings
    orig_offset = 0
    trans_offset = orig_len
    # Build tables
    orig_table = struct.pack("<II", orig_len, orig_offset)
    trans_table = struct.pack("<II", trans_len, trans_offset)
    # Combine
    data = orig + trans
    # Header
    header = struct.pack("<IIIIIII", magic, revision, nstrings, 8 + 8 + 8 + 8 + 8, 8 + 8 + 8 + 8 + 8 + 8, 0, 0)
    with open(path, 'wb') as f:
        f.write(header)
        f.write(orig_table)
        f.write(trans_table)
        f.write(data)

def test_load_gettext_translations_normal(tmp_path):
    # Create a locale directory with a valid .mo file
    locale_dir = tmp_path / "locale"
    locale_dir.mkdir()
    lang_dir = locale_dir / "es_ES" / "LC_MESSAGES"
    lang_dir.mkdir(parents=True)
    mo_path = lang_dir / "mydomain.mo"
    _create_mo_file(mo_path, "hello", "hola")
    # Call the function
    load_gettext_translations(str(locale_dir), "mydomain")
    # Verify that the translation is loaded
    assert _use_gettext is True
    assert "es_ES" in _supported_locales
    assert "es_ES" in _translations
    trans = _translations["es_ES"]
    assert trans.gettext("hello") == "hola"

def test_load_gettext_translations_missing_file(tmp_path):
    # Create a locale directory without any .mo files
    locale_dir = tmp_path / "empty_locale"
    locale_dir.mkdir()
    # Call the function
    load_gettext_translations(str(locale_dir), "nonexistent")
    # Should only contain the default locale
    assert _supported_locales == frozenset([_default_locale])
    assert _translations == {}

def test_load_gettext_translations_invalid_file(tmp_path):
    # Create a locale directory with an invalid .mo file
    locale_dir = tmp_path / "bad_locale"
    locale_dir.mkdir()
    bad_dir = locale_dir / "fr_FR" / "LC_MESSAGES"
    bad_dir.mkdir(parents=True)
    bad_mo = bad_dir / "mydomain.mo"
    # Write random bytes to make it invalid
    bad_mo.write_bytes(b"not a valid mo file")
    # Call the function
    load_gettext_translations(str(locale_dir), "mydomain")
    # The invalid file should be skipped, leaving only default locale
    assert _supported_locales == frozenset([_default_locale])
    assert _translations == {}
