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

def test_basic_translation_returns_translated_message():
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)
    # Simple message translation
    result = locale.translate("hello")
    assert result == "translated:hello"
    # Ensure that plural form is not used when plural_message is None
    result_no_plural = locale.translate("item")
    assert result_no_plural == "translated:item"

def test_plural_translation_returns_correct_form():
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)
    # Singular case
    singular = locale.translate("apple", plural_message="apples", count=1)
    assert singular == "apple"
    # Plural case
    plural = locale.translate("apple", plural_message="apples", count=3)
    assert plural == "apples"

def test_context_translation_fallback_and_plural_context():
    translations = DummyTranslations()
    locale = GettextLocale("en", translations)
    # Context with no translation (fallback to original)
    context_msg = locale.pgettext("law", "right")
    assert context_msg == "right"
    # Context with translation (simulate by overriding gettext to return context)
    def custom_gettext(msg):
        if msg == "law" + CONTEXT_SEPARATOR + "right":
            return "law_right"
        return f"translated:{msg}"
    translations.gettext = custom_gettext
    context_msg_translated = locale.pgettext("law", "right")
    assert context_msg_translated == "law_right"
    # Plural context: use custom ngettext to return context-specific plural
    def custom_ngettext(singular, plural, n):
        if singular == "law" + CONTEXT_SEPARATOR + "club":
            return "law_club" if n == 1 else "law_clubs"
        return singular if n == 1 else plural
    translations.ngettext = custom_ngettext
    plural_context = locale.pgettext("law", "club", "clubs", count=2)
    assert plural_context == "law_clubs"
