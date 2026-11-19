import gettext
import pytest
from tornado.locale import GettextLocale, CONTEXT_SEPARATOR

class DummyTranslations:
    """Simple translations that echo the message or plural form."""
    def gettext(self, msg):
        # For context messages, strip context separator if present
        if CONTEXT_SEPARATOR in msg:
            return msg.split(CONTEXT_SEPARATOR, 1)[1]
        return msg

    def ngettext(self, singular, plural, n):
        return singular if n == 1 else plural

def test_translate_and_plural():
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)

    # Singular translation
    assert locale.translate("hello") == "hello"

    # Plural translation with count 1
    assert locale.translate("apple", "apples", 1) == "apple"

    # Plural translation with count 2
    assert locale.translate("apple", "apples", 2) == "apples"

    # Boundary: count zero should use plural form
    assert locale.translate("apple", "apples", 0) == "apples"

def test_pgettext_with_context_and_plural():
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)

    # Context present, singular
    assert locale.pgettext("fruit", "apple") == "apple"

    # Context present, plural with count 1
    assert locale.pgettext("fruit", "apple", "apples", 1) == "apple"

    # Context present, plural with count 3
    assert locale.pgettext("fruit", "apple", "apples", 3) == "apples"

def test_pgettext_context_not_found():
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)

    # Simulate missing context by returning the original message with separator
    # DummyTranslations.gettext returns the message unchanged if separator present
    # So pgettext should detect separator in result and fallback to original
    # We use a context that will not be stripped by DummyTranslations
    # because DummyTranslations splits on separator and returns the part after it.
    # To force fallback, we modify DummyTranslations to return the full string.
    class BadContextTranslations:
        def gettext(self, msg):
            return msg  # return unchanged, simulating missing translation

        def ngettext(self, singular, plural, n):
            return singular if n == 1 else plural

    bad_translations = BadContextTranslations()
    bad_locale = GettextLocale("en", bad_translations)

    # Context not found: should return original message
    assert bad_locale.pgettext("unknown", "hello") == "hello"

    # Plural context not found: should fallback to singular/plural logic
    assert bad_locale.pgettext("unknown", "apple", "apples", 2) == "apples"
