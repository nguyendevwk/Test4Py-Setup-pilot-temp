import gettext
import pytest
from tornado.locale import GettextLocale, CONTEXT_SEPARATOR

class DummyTranslations(gettext.NullTranslations):
    """A minimal translation that records calls and returns predictable strings."""
    def gettext(self, message):
        # Return the message prefixed to indicate translation
        return f"translated:{message}"

    def ngettext(self, singular, plural, n):
        # Return singular or plural based on n
        return singular if n == 1 else plural

def test_gettextlocale_basic_translation():
    """Verify that a simple message is translated via gettext."""
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)
    result = locale.translate("hello")
    assert result == "translated:hello"

def test_gettextlocale_plural_translation():
    """Verify that plural forms are handled correctly."""
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)
    singular = "apple"
    plural = "apples"
    # Count 1 should return singular
    assert locale.translate(singular, plural_message=plural, count=1) == singular
    # Count 2 should return plural
    assert locale.translate(singular, plural_message=plural, count=2) == plural

def test_gettextlocale_context_translation():
    """Verify that context-aware translations work and fallback correctly."""
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)
    context = "fruit"
    message = "apple"
    # Context translation should prepend context and separator
    expected_context_msg = f"{context}{CONTEXT_SEPARATOR}{message}"
    result = locale.pgettext(context, message)
    assert result == f"translated:{expected_context_msg}"
    # If plural context is requested, ngettext should be used
    plural = "apples"
    result_plural = locale.pgettext(context, message, plural_message=plural, count=3)
    assert result_plural == plural
