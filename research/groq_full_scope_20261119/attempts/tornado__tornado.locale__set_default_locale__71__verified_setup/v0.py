import pytest
import importlib
import types

# Import the target module
locale_module = importlib.import_module("tornado.locale")

# Helper to reset module globals between tests
def reset_globals():
    if hasattr(locale_module, "_default_locale"):
        del locale_module._default_locale
    if hasattr(locale_module, "_supported_locales"):
        del locale_module._supported_locales
    if hasattr(locale_module, "_translations"):
        # Preserve original translations for consistency
        pass

def test_set_default_locale_updates_globals_and_supported():
    """Calling set_default_locale with a valid language code updates
    the module globals and includes the code in the supported locales set."""
    reset_globals()
    # Ensure initial state
    assert not hasattr(locale_module, "_default_locale")
    assert not hasattr(locale_module, "_supported_locales")

    # Call with a typical locale code
    locale_module.set_default_locale("en_US")

    # Check that the globals are set correctly
    assert locale_module._default_locale == "en_US"
    assert isinstance(locale_module._supported_locales, frozenset)
    # The supported locales should contain the new default
    assert "en_US" in locale_module._supported_locales
    # It should also contain any existing translation keys
    existing_keys = set(locale_module._translations.keys())
    assert existing_keys.issubset(locale_module._supported_locales)

def test_set_default_locale_with_empty_string():
    """An empty string is accepted as a locale code and is added to the
    supported locales set."""
    reset_globals()
    locale_module.set_default_locale("")
    assert locale_module._default_locale == ""
    assert "" in locale_module._supported_locales
    # The set should still be a frozenset
    assert isinstance(locale_module._supported_locales, frozenset)

def test_set_default_locale_with_none_raises_type_error():
    """Passing None should raise a TypeError because the function expects
    a string and later code may use string methods on the default locale."""
    reset_globals()
    with pytest.raises(TypeError):
        locale_module.set_default_locale(None)
