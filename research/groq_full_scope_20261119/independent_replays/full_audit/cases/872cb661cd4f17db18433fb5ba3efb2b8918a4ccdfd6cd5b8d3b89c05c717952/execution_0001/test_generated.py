import os
import glob
import gettext
import importlib
import tempfile
import shutil
import pytest
from pathlib import Path

# Import the target function and the module globals
import tornado.locale as locale_module

@pytest.fixture
def tmp_locale_dir(tmp_path):
    """Create a temporary locale directory structure."""
    return tmp_path

def test_load_gettext_translations_no_files(tmp_locale_dir):
    """When no .mo files exist, the function should set _use_gettext to True
    and _supported_locales to contain only the default locale."""
    # Ensure the directory is empty
    locale_module.load_gettext_translations(str(tmp_locale_dir), "dummy")
    # _translations should be empty
    assert locale_module._translations == {}
    # _use_gettext should be True
    assert locale_module._use_gettext is True
    # _supported_locales should contain the default locale only
    assert locale_module._supported_locales == frozenset([locale_module._default_locale])

def test_load_gettext_translations_with_valid_mo(tmp_locale_dir):
    """When a valid .mo file is present, it should be loaded into _translations."""
    # Create a minimal locale tree with a valid .mo file
    lang_dir = tmp_locale_dir / "en" / "LC_MESSAGES"
    lang_dir.mkdir(parents=True)
    mo_path = lang_dir / "test.mo"

    # Create a simple .mo file using gettext.GNUTranslations
    # We use a minimal .po content and compile it to .mo
    po_content = """
msgid ""
msgstr ""
"Language: en\\n"

msgid "hello"
msgstr "hello"
"""
    po_path = lang_dir / "test.po"
    po_path.write_text(po_content, encoding="utf-8")
    # Compile the .po to .mo
    import subprocess
    subprocess.run(["msgfmt", str(po_path), "-o", str(mo_path)], check=True)

    locale_module.load_gettext_translations(str(tmp_locale_dir), "test")

    # The translation for 'en' should be loaded
    assert "en" in locale_module._translations
    trans = locale_module._translations["en"]
    # The translation should correctly translate the string
    assert trans.gettext("hello") == "hello"

def test_load_gettext_translations_invalid_file(tmp_locale_dir, caplog):
    """If a .mo file is invalid, the function should log an error and skip it."""
    # Create an invalid .mo file
    lang_dir = tmp_locale_dir / "fr" / "LC_MESSAGES"
    lang_dir.mkdir(parents=True)
    mo_path = lang_dir / "invalid.mo"
    mo_path.write_bytes(b"not a valid mo file")

    with caplog.at_level("ERROR"):
        locale_module.load_gettext_translations(str(tmp_locale_dir), "invalid")

    # No translations should be loaded
    assert locale_module._translations == {}
    # An error should have been logged
    assert any(
        "Cannot load translation for 'fr'" in record.message for record in caplog.records
    )
