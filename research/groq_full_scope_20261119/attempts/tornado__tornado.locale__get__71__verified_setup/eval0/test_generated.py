import pytest
from tornado import locale

def test_get_returns_locale_with_exact_match():
    """`get` should return a Locale instance that matches the exact code."""
    loc = locale.get("en_US")
    # The returned object should be an instance of Locale
    assert isinstance(loc, locale.Locale)
    # The language attribute should match the requested code
    assert getattr(loc, "language", None) == "en_US"

def test_get_falls_back_to_default_for_unknown_locale():
    """If no matching locale is found, `get` should return the default locale."""
    # Use a locale code that is almost certainly not present
    loc = locale.get("xx_YY")
    # The default locale is en_US unless changed
    assert getattr(loc, "language", None) == "en_US"

def test_get_selects_first_matching_locale_in_list():
    """`get` should iterate over the provided codes and return the first match."""
    # Provide an unknown code first, then a known one
    loc = locale.get("xx_YY", "en_GB")
    assert isinstance(loc, locale.Locale)
    assert getattr(loc, "language", None) == "en_GB"
