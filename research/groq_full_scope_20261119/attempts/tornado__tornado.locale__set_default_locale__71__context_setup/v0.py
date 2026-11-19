import importlib
import types
import pytest

# Import the module under test
import tornado.locale as locale_module


def reset_globals():
    """Reset the module globals to their original state."""
    locale_module._default_locale = "en_US"
    locale_module._translations = {}
    locale_module._supported_locales = frozenset(["en_US"])


def test_set_default_locale_updates_globals_and_supported_locales():
    """Normal case: setting a new locale updates globals and supported locales."""
    reset_globals()
    # Ensure initial state
    assert locale_module._default_locale == "en_US"
    assert locale_module._supported_locales == frozenset(["en_US"])

    # Set a new default locale
    locale_module.set_default_locale("fr_FR")

    # Verify that the default locale is updated
    assert locale_module._default_locale == "fr_FR"

    # Verify that supported locales now include the new locale
    assert "fr_FR" in locale_module._supported_locales
    # The original locale should still be present
    assert "en_US" in locale_module._supported_locales
    # The supported locales should be a frozenset
    assert isinstance(locale_module._supported_locales, frozenset)


def test_set_default_locale_with_empty_string():
    """Boundary case: setting an empty string as locale."""
    reset_globals()
    locale_module.set_default_locale("")

    # The default locale should be the empty string
    assert locale_module._default_locale == ""
    # Supported locales should contain the empty string
    assert "" in locale_module._supported_locales
    # The original locale should still be present
    assert "en_US" in locale_module._supported_locales


def test_set_default_locale_with_non_string_raises_type_error():
    """Error case: passing a non-string should raise a TypeError."""
    reset_globals()
    with pytest.raises(TypeError):
        locale_module.set_default_locale(123)  # type: ignore[arg-type]
