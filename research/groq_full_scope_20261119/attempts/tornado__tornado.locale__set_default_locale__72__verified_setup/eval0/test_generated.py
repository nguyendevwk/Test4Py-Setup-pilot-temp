import importlib
import pytest

# Import the module under test
import tornado.locale as locale_module


def reload_locale():
    """Reload the locale module to reset its global state."""
    importlib.reload(locale_module)
    return locale_module


def test_set_default_locale_normal():
    """Test that set_default_locale correctly updates globals with a typical locale code."""
    mod = reload_locale()
    # Ensure initial state is not the test locale
    assert getattr(mod, "_default_locale", None) != "en_US"
    # Call the function
    mod.set_default_locale("en_US")
    # Check that the default locale is set
    assert mod._default_locale == "en_US"
    # _supported_locales should include the new default and all translation keys
    expected = frozenset(list(mod._translations.keys()) + ["en_US"])
    assert mod._supported_locales == expected
    # Ensure that the default locale is not in the translations dict
    assert "en_US" not in mod._translations


def test_set_default_locale_empty_string():
    """Test that an empty string is accepted as a locale code."""
    mod = reload_locale()
    mod.set_default_locale("")
    # The default locale should be the empty string
    assert mod._default_locale == ""
    # The supported locales should include the empty string
    assert "" in mod._supported_locales
    # The empty string should not be a key in the translations dict
    assert "" not in mod._translations


def test_set_default_locale_non_string():
    """Test that passing a non-string value does not raise and updates globals accordingly."""
    mod = reload_locale()
    # Use an integer as the locale code
    mod.set_default_locale(42)
    # The default locale should be set to the integer
    assert mod._default_locale == 42
    # The supported locales should include the integer
    assert 42 in mod._supported_locales
    # The integer should not be a key in the translations dict
    assert 42 not in mod._translations
