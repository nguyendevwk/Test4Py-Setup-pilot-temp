import pytest
from tornado.locale import get, Locale

def test_default_locale_returns_en_us(tmp_path):
    # Calling get() with no arguments should return the default locale,
    # which is en_US by default.
    locale = get()
    assert isinstance(locale, Locale)
    assert locale.language == "en"
    assert locale.country == "US"
    # The default locale should have a non-empty translations dictionary
    assert isinstance(locale.translations, dict)
    assert locale.translations  # should not be empty

def test_specific_locale_returns_correct_language_and_country(tmp_path):
    # Requesting a specific locale should return a Locale with matching
    # language and country codes.
    locale = get("fr_FR")
    assert isinstance(locale, Locale)
    assert locale.language == "fr"
    assert locale.country == "FR"
    # The translations dictionary should contain at least one entry
    # (the default empty string key is always present).
    assert isinstance(locale.translations, dict)
    assert "" in locale.translations

def test_multiple_codes_prioritizes_first_match(tmp_path):
    # When multiple locale codes are provided, the first matching locale
    # should be returned. If the first code is not available, the next
    # one should be used.
    # Assume "xx_YY" is not a valid locale, so the function should fall
    # back to "en_US".
    locale = get("xx_YY", "en_US")
    assert isinstance(locale, Locale)
    assert locale.language == "en"
    assert locale.country == "US"
    # Verify that the fallback did not use the invalid code
    assert locale.translations  # should be non-empty
