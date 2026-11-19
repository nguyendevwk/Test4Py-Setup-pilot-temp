import pytest
from tornado.locale import set_default_locale, _default_locale, _supported_locales, _translations

def test_set_default_locale_basic(tmp_path):
    """Setting a new default locale updates the globals correctly."""
    set_default_locale("en_US")
    assert _default_locale == "en_US"
    # _supported_locales should contain the new default and all existing translation keys
    expected = frozenset(list(_translations.keys()) + ["en_US"])
    assert _supported_locales == expected

def test_set_default_locale_updates_supported(tmp_path):
    """Changing the default locale updates the supported locales set."""
    # Capture current supported locales
    original = _supported_locales
    set_default_locale("fr_FR")
    assert _default_locale == "fr_FR"
    # The new set should be the original plus the new default
    expected = frozenset(list(_translations.keys()) + ["fr_FR"])
    assert _supported_locales == expected
    # Ensure the original set is not mutated
    assert original != _supported_locales

def test_set_default_locale_idempotent(tmp_path):
    """Calling set_default_locale with the same value is idempotent."""
    set_default_locale("de_DE")
    first_set = _supported_locales
    set_default_locale("de_DE")
    second_set = _supported_locales
    assert first_set == second_set
    assert _default_locale == "de_DE"
