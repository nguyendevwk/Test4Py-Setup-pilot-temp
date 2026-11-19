import gettext
import pytest
from tornado.locale import GettextLocale, CONTEXT_SEPARATOR

class DummyTranslations:
    """Simple translations object mimicking gettext.NullTranslations."""
    def gettext(self, msgid: str) -> str:
        # Return the msgid unchanged unless it contains the context separator
        if CONTEXT_SEPARATOR in msgid:
            # Simulate missing translation by returning the original msgid
            return msgid
        return f"translated:{msgid}"

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        # Return singular or plural based on n
        return singular if n == 1 else plural

def test_translate_singular_and_plural():
    """Test GettextLocale.translate handles singular and plural correctly."""
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)
    # Singular translation
    assert locale.translate("hello") == "translated:hello"
    # Plural translation with count 1
    assert locale.translate("apple", "apples", 1) == "apple"
    # Plural translation with count 2
    assert locale.translate("apple", "apples", 2) == "apples"

def test_pgettext_context_found_and_missing():
    """Test GettextLocale.pgettext with context that is found and not found."""
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)
    # Context found: gettext returns a string without separator
    result_found = locale.pgettext("greeting", "hello")
    assert result_found == "translated:greeting\x04hello"
    # Context missing: gettext returns the original msgid containing separator
    # We simulate missing by having DummyTranslations return the msgid unchanged
    # when it contains the separator. The fallback should return the original message.
    result_missing = locale.pgettext("missing", "hello")
    assert result_missing == "hello"

def test_pgettext_plural_with_context_and_fallback():
    """Test GettextLocale.pgettext with plural forms and context fallback."""
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)
    # Context found for plural: ngettext returns the plural form
    result = locale.pgettext("item", "apple", "apples", 3)
    assert result == "apples"
    # Context missing for plural: fallback to normal ngettext
    # Simulate missing by having DummyTranslations return msgid with separator
    # The fallback should still return the plural form
    result_fallback = locale.pgettext("missing", "apple", "apples", 1)
    assert result_fallback == "apple"
