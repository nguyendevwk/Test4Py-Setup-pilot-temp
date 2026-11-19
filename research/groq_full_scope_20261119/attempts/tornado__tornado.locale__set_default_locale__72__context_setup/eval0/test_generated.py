import pytest
from tornado.locale import set_default_locale, _default_locale, _supported_locales, _translations

def test_set_default_locale_updates_globals():
    # Initial state
    original_default = _default_locale
    original_supported = set(_supported_locales)

    # Set a new locale
    new_locale = "fr_FR"
    set_default_locale(new_locale)

    # Assert that the default locale is updated
    assert _default_locale == new_locale

    # Assert that the new locale is added to the supported set
    assert new_locale in _supported_locales

    # Assert that the supported set contains all original locales plus the new one
    assert original_supported.union({new_locale}) == set(_supported_locales)

    # Reset to original state for isolation
    set_default_locale(original_default)

def test_set_default_locale_with_non_string_code():
    # Passing an integer should not raise an exception
    int_code = 123
    set_default_locale(int_code)

    # The default locale should now be the integer value
    assert _default_locale == int_code

    # The supported locales should include the integer
    assert int_code in _supported_locales

    # Reset to a string for isolation
    set_default_locale("en_US")

def test_set_default_locale_does_not_modify_translations():
    # Capture the current translations mapping
    original_translations = _translations.copy()

    # Set a new locale
    set_default_locale("es_ES")

    # Ensure the translations dictionary remains unchanged
    assert _translations == original_translations
