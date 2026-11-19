import os
import shutil
import tempfile
import pytest
from tornado import locale
from tornado._locale_data import LOCALE_NAMES

# Helper to create a minimal .mo file for a custom locale
def _create_mo_file(tmp_path, lang_code, msgid, msgstr):
    import polib
    po = polib.POFile()
    po.metadata = {
        'Project-Id-Version': '1',
        'Language': lang_code,
    }
    entry = polib.POEntry(msgid=msgid, msgstr=msgstr)
    po.append(entry)
    po_path = tmp_path / f"{lang_code}.po"
    po.save(po_path)
    po_path = po_path.with_suffix('.mo')
    po.save_as_mofile(po_path)
    return po_path

@pytest.fixture
def custom_locale_dir(tmp_path):
    """Create a temporary locale directory with a custom locale."""
    locale_dir = tmp_path / "locale"
    locale_dir.mkdir()
    # Create a simple .mo file for language 'xx_YY'
    _create_mo_file(locale_dir, "xx_YY", "hello", "hola")
    # Add the directory to the locale search path
    original_paths = locale._locale_paths.copy()
    locale._locale_paths.insert(0, str(locale_dir))
    yield locale_dir
    # Restore original paths
    locale._locale_paths = original_paths

def test_get_returns_closest_match(custom_locale_dir):
    """When a matching locale exists, get should return that locale."""
    # The custom locale 'xx_YY' should be found
    loc = locale.get("xx_YY")
    assert loc.language == "xx_YY"
    # Verify that translation works
    assert loc.translate("hello") == "hola"

def test_get_defaults_to_en_US_when_no_match():
    """If no locale matches, get should fall back to the default locale."""
    # Use a nonsense locale code that is unlikely to exist
    loc = locale.get("zz_ZZ")
    # Default locale is en_US
    assert loc.language == "en_US"
    # The translation of a known string should be the original string
    assert loc.translate("hello") == "hello"

def test_get_handles_empty_and_invalid_inputs():
    """Calling get with no arguments or invalid strings should return default."""
    # No arguments: should return default
    loc_default = locale.get()
    assert loc_default.language == "en_US"

    # Empty string: should also return default
    loc_empty = locale.get("")
    assert loc_empty.language == "en_US"

    # Passing a non-existent locale with a fallback list
    loc_fallback = locale.get("nonexistent", "en_GB")
    # en_GB exists in LOCALE_NAMES, so it should be returned
    assert loc_fallback.language == "en_GB"
