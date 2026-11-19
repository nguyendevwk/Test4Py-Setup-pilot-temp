import pytest
import importlib
import sys

# Import the target module
tornado_locale = importlib.import_module("tornado.locale")

def test_set_default_locale_updates_globals_and_supported_locales():
    # Ensure initial state is not affected by the test
    original_default = getattr(tornado_locale, "_default_locale", None)
    original_supported = getattr(tornado_locale, "_supported_locales", None)

    # Call with a new locale code
    tornado_locale.set_default_locale("fr")
    assert tornado_locale._default_locale == "fr"
    # The supported locales should now include the new default
    assert "fr" in tornado_locale._supported_locales
    # It should also include any existing translations
    for key in tornado_locale._translations:
        assert key in tornado_locale._supported_locales

    # Restore original state
    if original_default is not None:
        tornado_locale._default_locale = original_default
    if original_supported is not None:
        tornado_locale._supported_locales = original_supported

def test_set_default_locale_with_empty_string():
    # Call with an empty string as locale code
    tornado_locale.set_default_locale("")
    assert tornado_locale._default_locale == ""
    # Empty string should be part of supported locales
    assert "" in tornado_locale._supported_locales

def test_set_default_locale_with_non_string_raises_type_error():
    # Passing a non-string should raise a TypeError when used as a key
    with pytest.raises(TypeError):
        tornado_locale.set_default_locale(123)  # type: ignore[arg-type]
