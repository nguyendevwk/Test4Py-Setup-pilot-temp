import gettext
import pytest
from tornado.locale import GettextLocale, CONTEXT_SEPARATOR


class DummyTranslations:
    """Simple translation object mimicking gettext.NullTranslations."""
    def gettext(self, msg):
        # Return a predictable transformation for testing
        return f"translated:{msg}"

    def ngettext(self, singular, plural, n):
        # Return singular or plural based on n
        return singular if n == 1 else plural


def test_translate_singular_and_plural():
    """Test that translate returns correct singular or plural form."""
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)

    # Singular
    result_singular = locale.translate("apple")
    assert result_singular == "translated:apple"

    # Plural with count 1
    result_plural_one = locale.translate("apple", "apples", count=1)
    assert result_plural_one == "apple"

    # Plural with count >1
    result_plural_many = locale.translate("apple", "apples", count=3)
    assert result_plural_many == "apples"


def test_pgettext_context_fallback():
    """Test that pgettext falls back to message when context translation missing."""
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)

    # Context translation missing: result should be original message
    result = locale.pgettext("law", "right")
    assert result == "right"

    # Context translation present: simulate by overriding gettext
    def gettext_with_context(msg):
        if msg.startswith("law"):
            return "law:right"
        return f"translated:{msg}"
    translations.gettext = gettext_with_context

    result_with_context = locale.pgettext("law", "right")
    assert result_with_context == "law:right"


def test_pgettext_plural_context_and_fallback():
    """Test plural pgettext with context and fallback when translation missing."""
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)

    # Context translation missing for plural: fallback to plural logic
    result = locale.pgettext("organization", "club", "clubs", count=2)
    assert result == "clubs"

    # Provide a context translation that includes the separator
    def gettext_with_context_plural(msg):
        if msg.startswith("organization"):
            # Simulate a translation that contains the separator, indicating missing
            return f"organization{CONTEXT_SEPARATOR}club"
        return f"translated:{msg}"
    translations.gettext = gettext_with_context_plural

    # Should fallback to plural logic
    result_fallback = locale.pgettext("organization", "club", "clubs", count=2)
    assert result_fallback == "clubs"
