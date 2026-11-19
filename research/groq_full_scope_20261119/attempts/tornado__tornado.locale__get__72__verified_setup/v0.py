import pytest
from tornado import locale

def test_get_returns_locale_with_expected_language():
    """`get` should return a Locale whose language matches the requested code."""
    loc = locale.get("en_US")
    # The Locale object should expose a language attribute that matches the code prefix
    assert isinstance(loc, locale.Locale)
    assert loc.language == "en"

def test_get_falls_back_to_default_when_no_match():
    """If no locale matches, `get` should return the default locale (en_US)."""
    loc = locale.get("zz_ZZ")  # unlikely to exist
    assert isinstance(loc, locale.Locale)
    # Default locale is en_US, so language should be 'en'
    assert loc.language == "en"

def test_get_prefers_first_matching_locale_in_list():
    """`get` should return the first locale that matches among the provided codes."""
    # 'fr_FR' is a known locale; 'zz_ZZ' is not
    loc = locale.get("zz_ZZ", "fr_FR")
    assert isinstance(loc, locale.Locale)
    assert loc.language == "fr"
